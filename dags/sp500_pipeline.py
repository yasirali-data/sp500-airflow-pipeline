from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def test_pipeline():
    print("S&P 500 pipeline is working!")


with DAG(
    dag_id="sp500_pipeline",
    start_date=datetime(2026, 8, 31),
    schedule=None,
    catchup=False,
    tags=["sp500", "data-engineering"],
) as dag:

    test_task = PythonOperator(
        task_id="test_pipeline",
        python_callable=test_pipeline,
    )