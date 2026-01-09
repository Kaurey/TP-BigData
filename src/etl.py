from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, count, sum as _sum
import os
import sys
from logs import logger

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("BigDataTP") \
    .config("spark.jars", "/opt/postgresql-42.6.0.jar") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

logger.info(">>> STARTING JOIN INGESTION (BRONZE)")

# Paths
DATA_DIR = "/app/data"
RAW_DIR = os.path.join(DATA_DIR, "raw")
BRONZE_DIR = os.path.join(DATA_DIR, "bronze")
SILVER_DIR = os.path.join(DATA_DIR, "silver")
GOLD_DIR = os.path.join(DATA_DIR, "gold")

# 1. INGESTION (BRONZE)
# ---------------------

# A. CSV: Transactions
logger.info("Reading Transactions CSV...")
df_trans = spark.read.option("header", "true").option("inferSchema", "true").csv(os.path.join(RAW_DIR, "transactions.csv"))
df_trans.write.mode("overwrite").parquet(os.path.join(BRONZE_DIR, "transactions"))

# B. JSON: Events
logger.info("Reading Events JSON...")
df_events = spark.read.option("multiline", "true").json(os.path.join(RAW_DIR, "events.json"))
df_events.write.mode("overwrite").parquet(os.path.join(BRONZE_DIR, "events"))

# C. Database: Users (PostgreSQL)
logger.info("Reading Users from Postgres...")
jdbc_url = "jdbc:postgresql://postgres:5432/bigdata_db"
connection_properties = {
    "user": "admin",
    "password": "password",
    "driver": "org.postgresql.Driver"
}
try:
    df_users = spark.read.jdbc(url=jdbc_url, table="users", properties=connection_properties)
    df_users.write.mode("overwrite").parquet(os.path.join(BRONZE_DIR, "users"))
except Exception as e:
    logger.error(f"Error reading from Postgres: {e}")
    # Fallback for unconnected testing if DB isn't ready immediately
    sys.exit(1)

logger.info(">>> BRONZE LAYER COMPLETE")


# 2. PROCESSING (SILVER)
# ----------------------
logger.info(">>> STARTING PROCESSING (SILVER)")

# Load Bronze
df_trans_b = spark.read.parquet(os.path.join(BRONZE_DIR, "transactions"))
df_users_b = spark.read.parquet(os.path.join(BRONZE_DIR, "users"))
df_events_b = spark.read.parquet(os.path.join(BRONZE_DIR, "events"))

# Clean & Enrich Transactions
# Join with Users to get metadata
df_trans_silver = df_trans_b.join(df_users_b, "user_id", "left") \
    .dropna() \
    .select("transaction_id", "user_id", "name", "country", "amount", "transaction_date")

df_trans_silver.write.mode("overwrite").parquet(os.path.join(SILVER_DIR, "transactions_enriched"))

# Clean Events
# Convert timestamp strings to actual timestamps if needed (inference usually works)
df_events_silver = df_events_b.dropna().select("event_id", "user_id", "event_type", "timestamp")
df_events_silver.write.mode("overwrite").parquet(os.path.join(SILVER_DIR, "events_cleaned"))

logger.info(">>> SILVER LAYER COMPLETE")


# 3. AGGREGATION (GOLD)
# ---------------------
logger.info(">>> STARTING AGGREGATION (GOLD)")

# Load Silver
df_sales = spark.read.parquet(os.path.join(SILVER_DIR, "transactions_enriched"))
df_log = spark.read.parquet(os.path.join(SILVER_DIR, "events_cleaned"))

# KPI 1: Total Sales per Country
kpi_country_sales = df_sales.groupBy("country").agg(_sum("amount").alias("total_sales"))
# Write as Parquet
kpi_country_sales.write.mode("overwrite").parquet(os.path.join(GOLD_DIR, "sales_by_country"))
# Also write as CSV for easy inspection if needed
kpi_country_sales.write.mode("overwrite").option("header", "true").csv(os.path.join(GOLD_DIR, "sales_by_country_csv"))

# KPI 2: Daily Sales
kpi_daily_sales = df_sales.groupBy("transaction_date").agg(_sum("amount").alias("daily_total")).orderBy("transaction_date")
kpi_daily_sales.write.mode("overwrite").parquet(os.path.join(GOLD_DIR, "sales_daily"))

# KPI 3: Event Distribution
kpi_events = df_log.groupBy("event_type").count()
kpi_events.write.mode("overwrite").parquet(os.path.join(GOLD_DIR, "events_distribution"))

logger.info(">>> GOLD LAYER COMPLETE")
logger.info(">>> ETL JOB FINISHED SUCCESSFULLY")

spark.stop()
