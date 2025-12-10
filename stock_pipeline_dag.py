from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from scripts.fetch_and_load import main as run_pipeline

default_args = {
    "owner": "abdul",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="stock_pipeline_dag",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",  # or "0 * * * *" for hourly
    catchup=False,
    tags=["stocks", "assignment"],
) as dag:

    fetch_and_load_task = PythonOperator(
        task_id="fetch_and_load_stock_data",
        python_callable=run_pipeline,
        op_kwargs={"symbol": "AAPL"},
    )
