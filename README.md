# S&P 500 Market Data Engineering Pipeline

An end-to-end data engineering pipeline that extracts S&P 500 stock market data from the Financial Modeling Prep (FMP) API, processes the data into JSON format, stores the raw data in Amazon S3, and loads it into Snowflake using Apache Airflow for workflow orchestration.

This project demonstrates a practical modern data engineering workflow involving API ingestion, cloud object storage, data warehousing, workflow orchestration, scheduling, retries, and containerization.

---

## 🚀 Project Overview

This project was built to simulate a real-world data engineering pipeline where financial market data is collected from an external API, temporarily stored in cloud object storage, and then loaded into a cloud data warehouse for analytics.

Apache Airflow is used to orchestrate and automate the complete workflow.

The pipeline follows this flow:

```text
FMP API
   │
   ▼
S&P 500 Symbols (~500)
   │
   ▼
Airflow Task 1
   │
   ▼
FMP API Data Extraction
(2 Symbols for Testing)
   │
   ▼
JSON File
   │
   ▼
Amazon S3
   │
   ▼
Snowflake


## 🎯 Project Objectives
The main objectives of this project are to:

Extract S&P 500 stock symbols from the FMP API
Retrieve financial market data using API requests
Build an automated ETL/ELT workflow using Apache Airflow
Convert extracted API data into JSON format
Store raw JSON data in Amazon S3
Establish a connection between Airflow and Snowflake
Load data from S3 into Snowflake
Schedule pipeline execution using Apache Airflow
Configure automatic task retries and retry delays
Containerize the development environment using Docker
Monitor pipeline execution through the Airflow UI


🏗️ Architecture
The pipeline uses a cloud-based architecture with Apache Airflow as the orchestration layer.

