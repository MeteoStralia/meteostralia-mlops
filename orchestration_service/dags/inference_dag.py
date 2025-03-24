from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator
from airflow.operators.docker_operator import DockerOperator
from docker.types import Mount
import os
#from airflow.operators.postgres_operator import PostgresOperator
import datetime

os.environ['PROJECTPATH'] = '/C:/Users/bruno/OneDrive/Documents/formation_data/projet_MLOPS/MeteoStralia/meteostralia-mlops'

with DAG(
    dag_id='inference_service',
    tags=['model', 'docker', 'meteostralia', 'datascientest'],
    default_args={
        'owner': 'airflow',
        'start_date': days_ago(2)  # A voir
    },
    schedule_interval=None, #'0 17 * * *', # A voir
    catchup=False) as dag:

        # new_data_sensor = FileSensor(
        #     task_id='new_data_sensor',
        #     filepath='./data/new_data/weatherAU_scrapdata_test.csv',
        #     poke_interval=20, # A voir
        #     #timeout=120, # A voir
        #     mode='poke' # A voir
        #     )
        
        def print_date_and_hello():
            print(datetime.datetime.now())
            print(os.getcwd())
            print('Hello from Airflow')

        hello = PythonOperator(
            task_id='hello',
            python_callable=print_date_and_hello, 
            dag = dag)


        inference = DockerOperator(
            task_id='inference',
            image='inference:latest',
            auto_remove=True,
            command='python3 src/inference_service/inference.py',
            docker_url=f"tcp://host.docker.internal:2375",
            network_mode="bridge",
            mounts=[
                Mount(source=os.environ['PROJECTPATH'] + '/data', 
                    target='/app/data', 
                    type='bind'),
                Mount(source=os.environ['PROJECTPATH'] + '/src', 
                    target='/app/src', 
                    type='bind'),
                Mount(source=os.environ['PROJECTPATH'] + '/models', 
                    target='/app/models', 
                    type='bind')
            ]
        )

hello >> inference
    
