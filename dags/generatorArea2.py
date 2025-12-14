from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow import DAG

from datetime import datetime

from producerArea2 import produceDataMonitor4, produceDataMonitor5, produceDataMonitor6

start_date = datetime(2020, 1, 1)
default_args = {
    'owner': 'GGCODE',
    'depends_on_past': False,
    'backfill': False,
    'start_date': start_date,
}

with DAG('generatorArea2',
         default_args=default_args,
         description='Area 2 Readings Generator',
         schedule_interval='@daily',
         catchup=False,
         start_date=start_date) as dag:

    start = EmptyOperator(task_id='start')

    m4 = PythonOperator(
        task_id='produceDataMonitor4',
        python_callable=produceDataMonitor4,
    )
    m5 = PythonOperator(
        task_id='produceDataMonitor5',
        python_callable=produceDataMonitor5,
    )
    m6 = PythonOperator(
        task_id='produceDataMonitor6',
        python_callable=produceDataMonitor6,
    )

    start >> [m4, m5, m6]