FROM python:3.9-slim-bookworm

# Install Java (Required for Spark) and other system dependencies
RUN apt-get update && \
    apt-get install -y openjdk-17-jre-headless curl procps && \
    rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download PostgreSQL JDBC Driver
RUN curl -o /opt/postgresql-42.6.0.jar https://jdbc.postgresql.org/download/postgresql-42.6.0.jar

# Set working directory
WORKDIR /app

# Copy source code
COPY src/ /app/src/

# Entrypoint default (can be overridden)
CMD ["bash"]
