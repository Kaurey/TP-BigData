import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time

# Page Config
st.set_page_config(page_title="Big Data Dashboard", layout="wide")

st.title("📊 TP Big Data - Results Dashboard")
st.markdown("Architecture: **Ingestion -> Bronze -> Silver -> Gold -> Visualization**")

# Paths inside Docker
GOLD_DIR = "data/gold"

def load_data():
    """Load Gold data from Parquet files."""
    try:
        sales_country = pd.read_parquet(os.path.join(GOLD_DIR, "sales_by_country"))
        sales_daily = pd.read_parquet(os.path.join(GOLD_DIR, "sales_daily"))
        events_dist = pd.read_parquet(os.path.join(GOLD_DIR, "events_distribution"))
        return sales_country, sales_daily, events_dist
    except Exception as e:
        return None, None, None

# Wait Loop for Data Availability
st.info("Waiting for data to be ready in 'data/gold'...")
placeholder = st.empty()

# Simple loading mechanism
sales_country, sales_daily, events_dist = load_data()

if sales_country is None or sales_country.empty:
    placeholder.warning("⚠️ Data not found yet. The ETL job might still be running. Please refresh in a few seconds.")
    if st.button("Reload Data"):
        st.experimental_rerun()
else:
    placeholder.success("✅ Data Loaded Successfully!")
    
    # KPIs Row
    st.subheader("Key Performance Indicators")
    col1, col2, col3 = st.columns(3)
    
    total_revenue = sales_country['total_sales'].sum()
    top_country = sales_country.loc[sales_country['total_sales'].idxmax()]['country']
    total_events = events_dist['count'].sum()
    
    col1.metric("Total Revenue", f"${total_revenue:,.2f}")
    col2.metric("Top Market", top_country)
    col3.metric("Total Events Handled", int(total_events))

    st.markdown("---")

    # Visualizations
    st.subheader("Visual Analytics")

    # Row 1
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("### Sales by Country")
        fig_bar = px.bar(sales_country, x='country', y='total_sales', color='country', 
                         title="Total Sales Revenue per Country",
                         labels={'total_sales': 'Revenue ($)', 'country': 'Country'})
        st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        st.markdown("### User Event Distribution")
        fig_pie = px.pie(events_dist, values='count', names='event_type', 
                         title="Distribution of User Events",
                         hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

    # Row 2
    st.markdown("### Daily Sales Trend")
    # Sort by date just in case
    sales_daily = sales_daily.sort_values(by="transaction_date")
    fig_line = px.line(sales_daily, x='transaction_date', y='daily_total', markers=True,
                       title="Revenue Evolution Over Time",
                       labels={'daily_total': 'Daily Revenue ($)', 'transaction_date': 'Date'})
    st.plotly_chart(fig_line, use_container_width=True)

    # Raw Data Section
    with st.expander("View Underlying Data (Gold Layer)"):
        st.write("Sales by Country:", sales_country)
        st.write("Daily Sales:", sales_daily)
