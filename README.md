# S&P 500 Data Engineering Pipeline

An end-to-end data engineering pipeline that extracts S&P 500 stock market data from the Financial Modeling Prep (FMP) API, stores the extracted data as JSON in Amazon S3, and loads the data into Snowflake using Apache Airflow for orchestration.

The project demonstrates a practical cloud-based data pipeline using API ingestion, workflow orchestration, cloud storage, data warehousing, scheduling, retries, and Docker.

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
        │  FMP API Call   │
        │   2 Symbols     │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │   JSON File     │
        │   Raw Data      │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │    Amazon S3    │
        │  Raw Storage    │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │    Snowflake    │
        │ Data Warehouse  │
        └─────────────────┘

📌 Project Overview
This project simulates a real-world financial data engineering workflow.

The pipeline uses approximately 500 S&P 500 stock symbols retrieved from the FMP API. During testing, the pipeline processes 2 symbols and retrieves their market data through the FMP API.

The extracted data is converted into JSON format, uploaded to Amazon S3, and then loaded into Snowflake.

Apache Airflow manages the complete workflow and automates task execution.

🔄 Pipeline Workflow
1. S&P 500 Symbol Extraction
The pipeline retrieves approximately 500 S&P 500 symbols from the FMP API.

These symbols are used as input for the downstream data extraction process.

2. Market Data Extraction
The next Airflow task sends requests to the FMP API.

For development and testing, 2 symbols are processed per pipeline execution

S&P 500 Symbols
       ↓
Select Symbols
       ↓
FMP API Request
       ↓
Market Data

3. JSON Processing
The API response is converted into JSON format.

The JSON file represents the raw extracted market data and acts as the intermediate data format before cloud storage.

4. Amazon S3
The generated JSON file is uploaded to an Amazon S3 bucket.

S3 is used as the raw/landing storage layer of the pipeline.

FMP API
   ↓
Python
   ↓
JSON
   ↓
Amazon S3

5. Snowflake
The pipeline establishes a connection with Snowflake and loads the data from the S3-based workflow into the Snowflake environment.

Snowflake serves as the cloud data warehouse for the project.

FMP API
   ↓
JSON
   ↓
Amazon S3
   ↓
Snowflake

⚙️ Apache Airflow
Apache Airflow is used to orchestrate the complete pipeline through a DAG.

The workflow is structured around dependent tasks:

Get S&P 500 Symbols
        ↓
Extract FMP Data
        ↓
Create JSON
        ↓
Upload to S3
        ↓
Load into Snowflake


Airflow handles:

Task dependencies
. Scheduling
. Retries
. Task execution
. Logging
. Pipeline monitoring

⏱️ Scheduling & Retry Configuration
The DAG was configured with the following settings during development and testing:

Configuration	     Value
Schedule	           Every 5 minutes
Retries	           2
Retry Delay	        2 minutes
DAG Owner	        Yasir

The 5-minute schedule was used for testing the pipeline repeatedly.

If a task fails, Airflow automatically retries the task up to 2 times, with a 2-minute delay between attempts.


🛠️ Tech Stack
Technology	                         Purpose
Python	                API extraction and data processing
Apache                   Airflow	Workflow orchestration
FMP API	                Financial market data source
Amazon S3	             Raw JSON storage
Snowflake	             Cloud data warehouse
PostgreSQL	             Airflow metadata database
Docker	                Containerization
Docker Compose	          Local multi-container environment
SQL	                   Data querying
Git & GitHub	          Version control


📁 Project Structure
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


🐳 Running Locally
Prerequisites
. Docker
. Docker Compose
. Git
. FMP API key
. AWS account with S3 bucket
. Snowflake account

Clone Repository

git clone https://github.com/yasirali-data/sp500-airflow-pipeline.git

cd sp500-airflow-pipeline

Build the Environment
docker compose build

Start Services
docker compose up -d

Check running containers:
docker compose ps


Initialize Airflow
If required by the project configuration:
docker compose up airflow-init

Then start the services:
docker compose up -d

Open Airflow
http://localhost:8080

The Airflow UI can be used to monitor DAG runs, task execution, logs, dependencies, and retries.

🔐 Credentials
The project requires credentials for external services such as:

FMP API
. AWS S3
. Snowflake
Sensitive credentials should never be committed to GitHub.

Use environment variables or Airflow Connections to manage credentials securely.

Example:

FMP_API_KEY
AWS_ACCESS_KEY
AWS_SECRET_KEY
SNOWFLAKE_ACCOUNT
SNOWFLAKE_USER
SNOWFLAKE_PASSWORD

Actual credentials are not included in this repository.

📊 Key Data Engineering Concepts
This project demonstrates practical experience with:

REST API data ingestion
Python-based data processing
ETL/ELT pipeline design
Apache Airflow DAGs
Workflow orchestration
Task dependencies
Automated scheduling
Retry and failure handling
Amazon S3 cloud storage
Snowflake data warehousing
Docker containerization
PostgreSQL
SQL
Git/GitHub
Cloud-based data pipeline architecture
🚀 Future Improvements
Possible improvements include:

Process all 500 S&P 500 symbols instead of the current 2-symbol test configuration
Implement incremental data ingestion
Add API rate-limit handling
Add data quality validation
Add automated testing
Implement Snowflake staging and production layers
Add CI/CD with GitHub Actions
Add Airflow failure notifications
Add monitoring and observability
Build analytical dashboards using Power BI
Deploy the pipeline to a cloud environment
💡 What This Project Demonstrates
This project demonstrates how to build an automated data pipeline that moves data from an external API into a cloud data warehouse:

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

It combines data ingestion, orchestration, cloud storage, data warehousing, scheduling, and fault tolerance into a single end-to-end data engineering workflow.

👨‍💻 Author
Yasir Ali

Data Engineering Enthusiast

Technologies: Python • SQL • Apache Airflow • AWS S3 • Snowflake • Docker • PostgreSQL • REST APIs

GitHub:
https://github.com/yasirali-data
