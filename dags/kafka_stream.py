from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 05, 9, 18, 31),
}

def get_data():
    import requests
    import json

    res = requests.get('https://randomuser.me/api/')
    res = res.json()
    res = res['results'][0]
    return res

def stream_data():
    import requests
    import json

    res = requests.get('https://randomuser.me/api/')
    res = res.json()
    user = res['results'][0]


with DAG('user_automation', 
         default_args=default_args, 
         schedule_interval='@daily', 
         catchup=False) as dag:
    stream_task = PythonOperator(
        task_id='stream_data_from_api',
        python_callable=stream_data,
        dag=dag,
    )


stream_data();