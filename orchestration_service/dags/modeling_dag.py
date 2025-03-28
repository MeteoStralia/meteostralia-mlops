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

# os.environ['PROJECTPATH'] = Variable.get("PROJECTPATH")
# os.environ['MLFLOW_TRACKING_USERNAME'] = Variable.get("MLFLOW_TRACKING_USERNAME")
# os.environ['MLFLOW_TRACKING_URI'] = Variable.get("MLFLOW_TRACKING_URI")

with DAG(
    dag_id='modeling_service',
    tags=['model', 'docker', 'meteostralia', 'datascientest'],
    default_args={
        'owner': 'airflow',
        'start_date': datetime.datetime(2021, 3 ,27, 8 ,0)  # tous les jours à 8h
    },
    schedule_interval= '0 8 * * *',
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
            docker_url=os.environ['AIRFLOW_DOCKER_HOST'],
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
            docker_url=os.environ['AIRFLOW_DOCKER_HOST'],
            network_mode="bridge",
            environment = {
                 'AIRFLOW_DAGSHUB_USER_TOKEN': os.environ['AIRFLOW_DAGSHUB_USER_TOKEN'],
                 'AIRFLOW_MLFLOW_TRACKING_USERNAME': os.environ['AIRFLOW_MLFLOW_TRACKING_USERNAME'],
                 'AIRFLOW_MLFLOW_TRACKING_URI': os.environ['AIRFLOW_MLFLOW_TRACKING_URI']
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

    
