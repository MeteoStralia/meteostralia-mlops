from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator
from airflow.operators.docker_operator import DockerOperator
from docker.types import Mount
import os
#from airflow.operators.postgres_operator import PostgresOperator
from datetime import date
import datetime
with DAG(
    dag_id='data_service',
    tags=['data', 'docker', 'meteostralia', 'datascientest'],
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


        reset_data = DockerOperator(
            task_id='reset_data',
            image='reset_data:latest',
            auto_remove=True,
            command='python3 src/data_service/ingest_data/reset_data.py',
            docker_url=f"tcp://host.docker.internal:2375", # a voir
            network_mode="bridge",
            #env_file = '../../docker.env',
            mounts=[
                Mount(source='/C:/Users/bruno/OneDrive/Documents/formation_data/projet_MLOPS/MeteoStralia/meteostralia-mlops/data', 
                    target='/app/data', 
                    type='bind'),
                Mount(source='/C:/Users/bruno/OneDrive/Documents/formation_data/projet_MLOPS/MeteoStralia/meteostralia-mlops/src', 
                    target='/app/src', 
                    type='bind')
            ]
        )

        ingest_new_data = DockerOperator(
            task_id='ingest_new_data',
            image='ingest_data:latest',
            auto_remove=True,
            command='python3 src/data_service/ingest_data/ingest_new_data.py',
            docker_url=f"tcp://host.docker.internal:2375", # a voir
            network_mode="bridge",
            #env_file = '../../docker.env',
            mounts=[
                Mount(source='/C:/Users/bruno/OneDrive/Documents/formation_data/projet_MLOPS/MeteoStralia/meteostralia-mlops/data', 
                    target='/app/data', 
                    type='bind'),
                Mount(source='/C:/Users/bruno/OneDrive/Documents/formation_data/projet_MLOPS/MeteoStralia/meteostralia-mlops/src', 
                    target='/app/src', 
                    type='bind')
            ]
        )
    
hello >> reset_data >> ingest_new_data
    
