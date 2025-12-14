from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow import DAG

from datetime import datetime

from producerArea1 import produceDataMonitor1, produceDataMonitor2, produceDataMonitor3

start_date = datetime(2020, 1, 1)
default_args = {
    'owner': 'GGCODE',
    'depends_on_past': False,
    'backfill': False,
    'start_date': start_date,
}

with DAG('generatorArea1',
         default_args=default_args,
         description='Area 1 Readings Generator',
         schedule_interval='@daily',
         catchup=False,
         start_date=start_date) as dag:

    start = EmptyOperator(task_id='start')

    m1 = PythonOperator(
        task_id='produceDataMonitor1',
        python_callable=produceDataMonitor1,
    )
    m2 = PythonOperator(
        task_id='produceDataMonitor2',
        python_callable=produceDataMonitor2,
    )
    m3 = PythonOperator(
        task_id='produceDataMonitor3',
        python_callable=produceDataMonitor3,
    )

    start >> [m1, m2, m3]