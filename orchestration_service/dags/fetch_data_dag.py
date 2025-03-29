from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator
from airflow.operators.docker_operator import DockerOperator
#from airflow.operators.postgres_operator import PostgresOperator
from docker.types import Mount
from airflow.models import Variable
import datetime
import subprocess
import pandas as pd

import os
from dotenv import load_dotenv

with DAG(
    dag_id='fetch_data',
    tags=['data', 'docker', 'meteostralia', 'datascientest'],
    default_args={
        'owner': 'airflow',
        'start_date': datetime.datetime(2021, 3 ,27, 8 ,0)  
    },
    schedule_interval= '0 8 * * *', # tous les jours à 8h
    catchup=False) as dag:

        def test():
            df = pd.read.csv("data/current_data/current_data.csv")
            print(df.head(10))

        fetch = DockerOperator(
                task_id='fetch_data',
                image='dvc_fetch:latest',
                auto_remove='success',
                command='python3 src/tracking_service/dvc/dvc_fetch.py',
                docker_url=os.environ['AIRFLOW_DOCKER_HOST'],
                network_mode="bridge",
                mounts=[
                    Mount(source=os.environ['PROJECTPATH'], 
                        target='/app', 
                        type='bind'),
                    Mount(source=os.environ['PROJECTPATH'] + '/data', 
                        target='/app/data', 
                        type='bind'),
                    Mount(source=os.environ['PROJECTPATH'] + '/src', 
                        target='/app/src', 
                        type='bind')
                ]
            )

        test_task = PythonOperator(
                task_id='hello',
                python_callable=test, 
                dag = dag)
        

fetch >> test_task