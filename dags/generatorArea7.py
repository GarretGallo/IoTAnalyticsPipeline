from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow import DAG

from datetime import datetime

from producerArea7 import produceDataMonitor19, produceDataMonitor20, produceDataMonitor21

start_date = datetime(2020, 1, 1)
default_args = {
    'owner': 'GGCODE',
    'depends_on_past': False,
    'backfill': False,
    'start_date': start_date,
}

with DAG('generatorArea7',
         default_args=default_args,
         description='Area 7 Readings Generator',
         schedule_interval='@daily',
         catchup=False,
         start_date=start_date) as dag:

    start = EmptyOperator(task_id='start')

    m19 = PythonOperator(
        task_id='produceDataMonitor19',
        python_callable=produceDataMonitor19,
    )
    m20 = PythonOperator(
        task_id='produceDataMonitor20',
        python_callable=produceDataMonitor20,
    )
    m21 = PythonOperator(
        task_id='produceDataMonitor21',
        python_callable=produceDataMonitor21,
    )

    start >> [m19, m20, m21]