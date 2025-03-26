from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator
from airflow.operators.docker_operator import DockerOperator
from docker.types import Mount
import os
#from airflow.operators.postgres_operator import PostgresOperator
import datetime
from airflow.models import Variable
from dotenv import load_dotenv

load_dotenv(dotenv_path='../params/general.env')
load_dotenv(dotenv_path='../params/docker.env')
load_dotenv(dotenv_path='../params/mlflow.env')
os.environ['PROJECTPATH'] = Variable.get("PROJECTPATH")

with DAG(
    dag_id='modeling_service',
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


        training = DockerOperator(
            task_id='training',
            image='training:latest',
            auto_remove='success',
            command='python3 src/modeling_service/training/train.py',
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

        evaluate = DockerOperator(
            task_id='evaluate',
            image='evaluate:latest',
            auto_remove='success',
            command='python3 src/modeling_service/evaluate/evaluate.py',
            docker_url=f"tcp://host.docker.internal:2375",
            network_mode="bridge",
            environment = {
                 'MLFLOW_TRACKING_USERNAME': os.environ['MLFLOW_TRACKING_USERNAME'],
                 'MLFLOW_TRACKING_URI': os.environ['MLFLOW_TRACKING_URI'],
                 'EXPERIMENT_NAME': os.environ["EXPERIMENT_NAME"],
                 'RUN_NAME' : os.environ["RUN_NAME"],
                 'ARTIFACT_PATH': os.environ["ARTIFACT_PATH"]

            },
            mounts=[
                Mount(source=os.environ['PROJECTPATH'] + '/data', 
                    target='/app/data', 
                    type='bind'),
                Mount(source=os.environ['PROJECTPATH'] + '/src', 
                    target='/app/src', 
                    type='bind'),
                Mount(source=os.environ['PROJECTPATH'] + '/models', 
                    target='/app/models', 
                    type='bind'),
                Mount(source=os.environ['PROJECTPATH'] + '/metrics', 
                    target='/app/metrics', 
                    type='bind')
            ]
        )

hello >> training >> evaluate

    
