from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow import DAG

from datetime import datetime

from producerArea6 import produceDataMonitor16, produceDataMonitor17, produceDataMonitor18

start_date = datetime(2020, 1, 1)
default_args = {
    'owner': 'GGCODE',
    'depends_on_past': False,
    'backfill': False,
    'start_date': start_date,
}

with DAG('generatorArea6',
         default_args=default_args,
         description='Area 6 Readings Generator',
         schedule_interval='@daily',
         catchup=False,
         start_date=start_date) as dag:

    start = EmptyOperator(task_id='start')

    m16 = PythonOperator(
        task_id='produceDataMonitor16',
        python_callable=produceDataMonitor16,
    )
    m17 = PythonOperator(
        task_id='produceDataMonitor17',
        python_callable=produceDataMonitor17,
    )
    m18 = PythonOperator(
        task_id='produceDataMonitor18',
        python_callable=produceDataMonitor18,
    )

    start >> [m16, m17, m18]