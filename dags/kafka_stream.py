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

def format_data(res):
    data = {}
    location = res['location']
    data['id'] = uuid.uuid4()
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{str(location['street']['number'])} {location['street']['name']}, " \
                      f"{location['city']}, {location['state']}, {location['country']}"
    data['post_code'] = location['postcode']
    data['email'] = res['email']
    data['username'] = res['login']['username']
    data['dob'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']

    return data

def stream_data():
    import json
    from kafka import KafkaProducer
    import time 

    res = get_data()
    res = format_data(res)

    producer = KafkaProducer(bootstrap_servers= ['localhost:9092'], max_block_ms=5000)
    producer.send('created_users', json.dumps(res).encode('utf-8'))

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