from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator

def dummy_python():
    print("Dummy python doing dummy things")

with DAG(
    "blacklist_failure_example",
    start_date=datetime(2024,1,1),
    max_active_runs=1,
    schedule_interval=None
) as dag:

    test_task = PythonOperator(
        task_id="test_task",
        python_callable=dummy_python
    )