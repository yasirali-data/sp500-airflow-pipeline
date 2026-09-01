# S&P 500 Data Engineering Pipeline

An end-to-end **data engineering pipeline** that extracts S&P 500 stock market data from the **Financial Modeling Prep (FMP) API)**, stores raw data as JSON in **Amazon S3**, and loads the data into **Snowflake** using **Apache Airflow** for workflow orchestration.

The project demonstrates a practical cloud data engineering workflow involving **API ingestion, Python, workflow orchestration, cloud storage, data warehousing, scheduling, retries, Docker, and SQL**.

---

## 🏗️ Architecture

```text
                    FMP API
                       │
                       ▼
              ┌─────────────────┐
              │ S&P 500 Symbols │
              │    ~500         │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Apache Airflow  │
              │      DAG        │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │   FMP API Call  │
              │  Test: 2 Stocks │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │   JSON Raw Data │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │    Amazon S3    │
              │  Raw / Landing  │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │    Snowflake    │
              │  Data Warehouse │
              └─────────────────┘
```

---

## 📌 Project Overview

This project simulates a real-world financial data engineering pipeline.

The pipeline retrieves approximately **500 S&P 500 stock symbols** from the FMP API. During development and testing, the downstream extraction process is configured to process **2 symbols per pipeline execution**.

The extracted market data is converted into JSON, uploaded to **Amazon S3**, and then loaded into **Snowflake**.

**Apache Airflow** orchestrates the complete workflow, manages task dependencies, schedules executions, and handles retries when tasks fail.

---

## 🔄 Pipeline Workflow

### 1. S&P 500 Symbol Extraction

The pipeline retrieves approximately 500 S&P 500 stock symbols from the FMP API.

These symbols provide the input for the downstream market data extraction process.

```text
FMP API
   ↓
S&P 500 Symbols
   ↓
Select Symbols
```

---

### 2. Market Data Extraction

The selected stock symbols are sent to the FMP API to retrieve market data.

For development and testing purposes, the pipeline currently processes **2 symbols per execution**.

```text
S&P 500 Symbols
       ↓
   Select Stocks
       ↓
    FMP API
       ↓
   Market Data
```

---

### 3. JSON Processing

The API response is processed using Python and converted into **JSON format**.

JSON is used as the raw intermediate data format before the data is stored in cloud storage.

```text
FMP API
   ↓
Python
   ↓
JSON
```

---

### 4. Amazon S3

The generated JSON data is uploaded to an **Amazon S3 bucket**.

S3 acts as the **raw/landing storage layer** of the pipeline.

```text
FMP API
   ↓
Python
   ↓
JSON
   ↓
Amazon S3
```

---

### 5. Snowflake

The pipeline connects to **Snowflake** and loads the extracted data into the cloud data warehouse.

Snowflake serves as the analytical data warehouse layer of the pipeline.

```text
FMP API
   ↓
JSON
   ↓
Amazon S3
   ↓
Snowflake
```

---

## ⚙️ Apache Airflow

Apache Airflow is used to orchestrate the pipeline through a DAG.

The workflow is organized into dependent tasks:

```text
Get S&P 500 Symbols
        ↓
Extract FMP Market Data
        ↓
Create JSON
        ↓
Upload to Amazon S3
        ↓
Load into Snowflake
```

Airflow provides:

* Task dependencies
* Scheduling
* Automatic retries
* Task execution
* Logging
* Pipeline monitoring

---

## ⏱️ Scheduling & Retry Configuration

The DAG was configured with the following settings during development and testing:

| Configuration | Value           |
| ------------- | --------------- |
| Schedule      | Every 5 minutes |
| Retries       | 2               |
| Retry Delay   | 2 minutes       |
| DAG Owner     | Yasir           |

The **5-minute schedule** was used during development to repeatedly test pipeline executions.

If a task fails, Airflow automatically retries the task up to **2 times**, with a **2-minute delay** between attempts.

---

## 🛠️ Tech Stack

| Technology         | Purpose                            |
| ------------------ | ---------------------------------- |
| **Python**         | API extraction and data processing |
| **Apache Airflow** | Workflow orchestration             |
| **FMP API**        | Financial market data source       |
| **Amazon S3**      | Raw/landing data storage           |
| **Snowflake**      | Cloud data warehouse               |
| **PostgreSQL**     | Airflow metadata database          |
| **Docker**         | Containerization                   |
| **Docker Compose** | Local multi-container environment  |
| **SQL**            | Data querying                      |
| **Git & GitHub**   | Version control                    |

---

## 📁 Project Structure

```text
sp500-airflow-pipeline/
│
├── dags/
│   └── sp500_pipeline.py
│
├── scripts/
│   └── ...
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🐳 Running Locally

### Prerequisites

Before running the project, make sure you have:

* Docker
* Docker Compose
* Git
* FMP API key
* AWS account with an S3 bucket
* Snowflake account

---

### 1. Clone the Repository

```bash
git clone https://github.com/yasirali-data/sp500-airflow-pipeline.git
```

```bash
cd sp500-airflow-pipeline
```

---

### 2. Build the Environment

```bash
docker compose build
```

---

### 3. Start the Services

```bash
docker compose up -d
```

---

### 4. Check Running Containers

```bash
docker compose ps
```

---

### 5. Initialize Airflow

If required by the project configuration:

```bash
docker compose up airflow-init
```

Then start the services:

```bash
docker compose up -d
```

---

### 6. Open Airflow

Once the services are running, open:

```text
http://localhost:8080
```

The Airflow UI can be used to monitor:

* DAG runs
* Task execution
* Task dependencies
* Logs
* Retries
* Pipeline status

---

## 🔐 Credentials & Environment Variables

The pipeline requires credentials for external services such as:

* FMP API
* Amazon S3
* Snowflake

**Never commit API keys, passwords, access keys, or other secrets to GitHub.**

Use environment variables or Airflow Connections to manage credentials securely.

Example environment variables:

```text
FMP_API_KEY
AWS_ACCESS_KEY
AWS_SECRET_KEY
SNOWFLAKE_ACCOUNT
SNOWFLAKE_USER
SNOWFLAKE_PASSWORD
```

Actual credentials are **not included** in this repository.

---

## 📊 Data Engineering Concepts Demonstrated

This project demonstrates practical experience with:

* REST API ingestion
* Python-based data extraction
* Data processing
* ETL/ELT pipeline design
* Apache Airflow DAGs
* Workflow orchestration
* Task dependencies
* Automated scheduling
* Retry and failure handling
* Amazon S3
* Snowflake
* Cloud data warehousing
* Docker containerization
* PostgreSQL
* SQL
* Git & GitHub
* Cloud-based data pipeline architecture

---

## 🚀 Future Improvements

The following improvements could extend the project further:

* [ ] Process all S&P 500 symbols instead of the current 2-symbol test configuration
* [ ] Implement incremental data ingestion
* [ ] Add API rate-limit handling
* [ ] Add data quality validation
* [ ] Add automated testing
* [ ] Implement Snowflake staging and production layers
* [ ] Add CI/CD using GitHub Actions
* [ ] Add Airflow failure notifications
* [ ] Improve pipeline monitoring and observability
* [ ] Build analytical dashboards using Power BI
* [ ] Deploy the pipeline to a cloud environment

---

## 🎯 What This Project Demonstrates

The project demonstrates how an automated data pipeline can move data from an external API into cloud storage and a cloud data warehouse.

```text
             FMP API
                ↓
              Python
                ↓
         Apache Airflow
                ↓
              JSON
                ↓
           Amazon S3
                ↓
            Snowflake
```

The pipeline combines **data ingestion, workflow orchestration, cloud storage, data warehousing, scheduling, retry handling, and containerization** into a single end-to-end data engineering workflow.

---

## 👨‍💻 Author

**Yasir Ali**

**Technologies:** Python • SQL • Apache Airflow • AWS S3 • Snowflake • Docker • PostgreSQL • REST APIs

**GitHub:** [yasiralii-dev](https://github.com/yasiralii-dev)
