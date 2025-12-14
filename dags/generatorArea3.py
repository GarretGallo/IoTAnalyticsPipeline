from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow import DAG

from datetime import datetime

from producerArea3 import produceDataMonitor7, produceDataMonitor8, produceDataMonitor9

start_date = datetime(2020, 1, 1)
default_args = {
    'owner': 'GGCODE',
    'depends_on_past': False,
    'backfill': False,
    'start_date': start_date,
}

with DAG('generatorArea3',
         default_args=default_args,
         description='Area 3 Readings Generator',
         schedule_interval='@daily',
         catchup=False,
         start_date=start_date) as dag:

    start = EmptyOperator(task_id='start')

    m7 = PythonOperator(
        task_id='produceDataMonitor7',
        python_callable=produceDataMonitor7,
    )
    m8 = PythonOperator(
        task_id='produceDataMonitor8',
        python_callable=produceDataMonitor8,
    )
    m9 = PythonOperator(
        task_id='produceDataMonitor9',
        python_callable=produceDataMonitor9,
    )

    start >> [m7, m8, m9]