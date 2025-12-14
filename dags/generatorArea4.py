from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow import DAG

from datetime import datetime

from producerArea4 import produceDataMonitor10, produceDataMonitor11, produceDataMonitor12

start_date = datetime(2020, 1, 1)
default_args = {
    'owner': 'GGCODE',
    'depends_on_past': False,
    'backfill': False,
    'start_date': start_date,
}

with DAG('generatorArea4',
         default_args=default_args,
         description='Area 4 Readings Generator',
         schedule_interval='@daily',
         catchup=False,
         start_date=start_date) as dag:

    start = EmptyOperator(task_id='start')

    m10 = PythonOperator(
        task_id='produceDataMonitor10',
        python_callable=produceDataMonitor10,
    )
    m11 = PythonOperator(
        task_id='produceDataMonitor11',
        python_callable=produceDataMonitor11,
    )
    m12 = PythonOperator(
        task_id='produceDataMonitor12',
        python_callable=produceDataMonitor12,
    )

    start >> [m10, m11, m12]