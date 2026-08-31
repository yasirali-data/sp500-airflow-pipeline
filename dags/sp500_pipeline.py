import sys
from datetime import datetime, timedelta

sys.path.insert(0, "/opt/airflow/scripts")

from airflow import DAG
from airflow.operators.python import PythonOperator

from extract_symbols import get_sp500_symbols
from fmp_api import fetch_profiles
from s3_upload import upload_to_s3
from load_snowflake import load_to_snowflake


default_args = {
    "owner": "you",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}


def fetch_and_upload(**context):
    fetch_profiles()

    # Use the DAG's logical date for a consistent S3 partition.
    upload_date = context["ds"]

    s3_key = upload_to_s3(upload_date=upload_date)

    return s3_key


def load_from_s3(**context):
    s3_key = context["ti"].xcom_pull(
        task_ids="fetch_fmp_and_upload_s3"
    )

    if not s3_key:
        raise ValueError("No S3 key received from Task 2")

    load_to_snowflake(s3_key=s3_key)


with DAG(
    dag_id="sp500_pipeline",
    default_args=default_args,
    start_date=datetime(2026, 8, 31),
    schedule="*/5 * * * *",
    catchup=False,
    tags=["sp500", "data-engineering"],
) as dag:

    task_1_get_symbols = PythonOperator(
        task_id="get_sp500_symbols",
        python_callable=get_sp500_symbols,
    )

    task_2_fetch_fmp_and_upload_s3 = PythonOperator(
        task_id="fetch_fmp_and_upload_s3",
        python_callable=fetch_and_upload,
    )

    task_3_load_snowflake = PythonOperator(
        task_id="load_data_to_snowflake",
        python_callable=load_from_s3,
    )

    task_1_get_symbols >> task_2_fetch_fmp_and_upload_s3 >> task_3_load_snowflake
