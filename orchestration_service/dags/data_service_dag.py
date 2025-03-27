from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator
from airflow.operators.docker_operator import DockerOperator
#from airflow.operators.postgres_operator import PostgresOperator
from docker.types import Mount
from airflow.models import Variable
import datetime

import os
from dotenv import load_dotenv

# load_dotenv(dotenv_path='general.env')
# load_dotenv(dotenv_path='docker.env')
# load_dotenv(dotenv_path='mlflow.env')
# os.environ['PROJECTPATH'] = Variable.get('projectpath')
# os.environ['PROJECTPATH'] = Variable.get('PROJECTPATH')

#os.environ['PROJECTPATH'] = os.environ['AIRFLOW_VAR_PROJECT_PATH']
#os.environ['PROJECTPATH'] = os.getenv('AIRFLOW_VAR_PROJECTPATH')

with DAG(
    dag_id='data_service',
    tags=['data', 'docker', 'meteostralia', 'datascientest'],
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


        reset_data = DockerOperator(
            task_id='reset_data',
            image='reset_data:latest',
            auto_remove='success',
            command='python3 src/data_service/ingest_data/reset_data.py',
            docker_url=f"tcp://host.docker.internal:2375",
            network_mode="bridge",
            mounts=[
                Mount(source=os.environ['PROJECTPATH'] + '/data', 
                    target='/app/data', 
                    type='bind'),
                Mount(source=os.environ['PROJECTPATH'] + '/src', 
                    target='/app/src', 
                    type='bind')
            ]
        )

        ingest_new_data = DockerOperator(
            task_id='ingest_new_data',
            image='ingest_data:latest',
            auto_remove='success',
            command='python3 src/data_service/ingest_data/ingest_new_data.py',
            docker_url=f"tcp://host.docker.internal:2375",
            network_mode="bridge",
            mounts=[
                Mount(source=os.environ['PROJECTPATH'] + '/data', 
                    target='/app/data', 
                    type='bind'),
                Mount(source=os.environ['PROJECTPATH'] + '/src', 
                    target='/app/src', 
                    type='bind')
            ]
        )

        complete_nas = DockerOperator(
            task_id='complete_nas',
            image='complete_nas:latest',
            auto_remove='success',
            command='python3 src/data_service/complete_nas/complete_nas.py',
            docker_url=f"tcp://host.docker.internal:2375",
            network_mode="bridge",
            mounts=[
                Mount(source=os.environ['PROJECTPATH'] + '/data', 
                    target='/app/data', 
                    type='bind'),
                Mount(source=os.environ['PROJECTPATH'] + '/src', 
                    target='/app/src', 
                    type='bind')
            ]
        )

        add_features = DockerOperator(
            task_id='add_features',
            image='features:latest',
            auto_remove='success',
            command='python3 src/data_service/features/add_features.py',
            docker_url=f"tcp://host.docker.internal:2375",
            network_mode="bridge",
            mounts=[
                Mount(source=os.environ['PROJECTPATH'] + '/data', 
                    target='/app/data', 
                    type='bind'),
                Mount(source=os.environ['PROJECTPATH'] + '/src', 
                    target='/app/src', 
                    type='bind')
            ]
        )

        encode_data = DockerOperator(
            task_id='encode_data',
            image='encode_data:latest',
            auto_remove='success',
            command='python3 src/data_service/encode_data/encode_data.py',
            docker_url=f"tcp://host.docker.internal:2375",
            network_mode="bridge",
            mounts=[
                Mount(source=os.environ['PROJECTPATH'] + '/data', 
                    target='/app/data', 
                    type='bind'),
                Mount(source=os.environ['PROJECTPATH'] + '/src', 
                    target='/app/src', 
                    type='bind')
            ]
        )

        split_data = DockerOperator(
            task_id='split_data',
            image='split_data:latest',
            auto_remove='success',
            command='python3 src/data_service/split_data/split_data.py',
            docker_url=f"tcp://host.docker.internal:2375",
            network_mode="bridge",
            mounts=[
                Mount(source=os.environ['PROJECTPATH'] + '/data', 
                    target='/app/data', 
                    type='bind'),
                Mount(source=os.environ['PROJECTPATH'] + '/src', 
                    target='/app/src', 
                    type='bind')
            ]
        )

        scale_data = DockerOperator(
            task_id='scale_data_data',
            image='scale_data:latest',
            auto_remove='success',
            command='python3 src/data_service/scale_data/scale_data.py',
            docker_url=f"tcp://host.docker.internal:2375",
            network_mode="bridge",
            mounts=[
                Mount(source=os.environ['PROJECTPATH'] + '/data', 
                    target='/app/data', 
                    type='bind'),
                Mount(source=os.environ['PROJECTPATH'] + '/src', 
                    target='/app/src', 
                    type='bind')
            ]
        )

hello >> reset_data >> ingest_new_data >> complete_nas >> add_features >> encode_data >> split_data >> scale_data
    
