from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow import DAG

from datetime import datetime

from producerArea5 import produceDataMonitor13, produceDataMonitor14, produceDataMonitor15

start_date = datetime(2020, 1, 1)
default_args = {
    'owner': 'GGCODE',
    'depends_on_past': False,
    'backfill': False,
    'start_date': start_date,
}

with DAG('generatorArea5',
         default_args=default_args,
         description='Area 5 Readings Generator',
         schedule_interval='@daily',
         catchup=False,
         start_date=start_date) as dag:

    start = EmptyOperator(task_id='start')

    m13 = PythonOperator(
        task_id='produceDataMonitor13',
        python_callable=produceDataMonitor13,
    )
    m14 = PythonOperator(
        task_id='produceDataMonitor14',
        python_callable=produceDataMonitor14,
    )
    m15 = PythonOperator(
        task_id='produceDataMonitor15',
        python_callable=produceDataMonitor15,
    )

    start >> [m13, m14, m15]