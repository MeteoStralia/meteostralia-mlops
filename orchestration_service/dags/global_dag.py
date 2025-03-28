from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator
from airflow.operators.docker_operator import DockerOperator
#from airflow.operators.postgres_operator import PostgresOperator
from docker.types import Mount
from airflow.models import Variable
import datetime
from airflow.utils.task_group import TaskGroup
import os

with DAG(
    dag_id='data_model_service',
    tags=['data', 'docker', 'meteostralia', 'datascientest'],
    default_args={
        'owner': 'airflow',
        'start_date': datetime.datetime(2021, 3 ,27, 8 ,0)  # tous les jours à 8h
    },
    schedule_interval= '0 8 * * *',
    catchup=False) as dag:
    
        def print_date_and_hello():
            print(datetime.datetime.now())
            print(os.getcwd())
            print('Hello from Airflow')

        hello = PythonOperator(
            task_id='hello',
            python_callable=print_date_and_hello, 
            dag = dag)
        
        with TaskGroup("Ingest_data_tasks") as Ingest_data_tasks:
            
            reset_data = DockerOperator(
                task_id='reset_data',
                image='meteostralia/meteorepo:reset_data'+os.environ["DOCKER_CURRENT_TAG"],
                auto_remove='success',
                command='python3 src/data_service/ingest_data/reset_data.py',
                docker_url=os.environ['AIRFLOW_DOCKER_HOST'],
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
                trigger_rule='all_success',
                task_id='ingest_new_data',
                image='meteostralia/meteorepo:ingest_data'+os.environ["DOCKER_CURRENT_TAG"],
                auto_remove='success',
                command='python3 src/data_service/ingest_data/ingest_new_data.py',
                docker_url=os.environ['AIRFLOW_DOCKER_HOST'],
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

            reset_data >> ingest_new_data 
    
        with TaskGroup("Preprocessing_tasks") as Preprocessing_tasks:

            complete_nas = DockerOperator(
                task_id='complete_nas',
                image='meteostralia/meteorepo:complete_nas'+os.environ["DOCKER_CURRENT_TAG"],
                auto_remove='success',
                command='python3 src/data_service/complete_nas/complete_nas.py',
                docker_url=os.environ['AIRFLOW_DOCKER_HOST'],
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
                image='meteostralia/meteorepo:features'+os.environ["DOCKER_CURRENT_TAG"],
                auto_remove='success',
                command='python3 src/data_service/features/add_features.py',
                docker_url=os.environ['AIRFLOW_DOCKER_HOST'],
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
                image='meteostralia/meteorepo:encode_data'+os.environ["DOCKER_CURRENT_TAG"],
                auto_remove='success',
                command='python3 src/data_service/encode_data/encode_data.py',
                docker_url=os.environ['AIRFLOW_DOCKER_HOST'],
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
                image='meteostralia/meteorepo:split_data'+os.environ["DOCKER_CURRENT_TAG"],
                auto_remove='success',
                command='python3 src/data_service/split_data/split_data.py',
                docker_url=os.environ['AIRFLOW_DOCKER_HOST'],
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
                image='meteostralia/meteorepo:scale_data'+os.environ["DOCKER_CURRENT_TAG"],
                auto_remove='success',
                command='python3 src/data_service/scale_data/scale_data.py',
                docker_url=os.environ['AIRFLOW_DOCKER_HOST'],
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
            complete_nas >> add_features >> encode_data >> split_data >> scale_data
        with TaskGroup("Modeling_tasks") as Modeling_tasks:
            training = DockerOperator(
            task_id='training',
            image='meteostralia/meteorepo:training'+os.environ["DOCKER_CURRENT_TAG"],
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
                image='meteostralia/meteorepo:evaluate'+os.environ["DOCKER_CURRENT_TAG"],
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
            training >> evaluate

        hello >> Ingest_data_tasks  >> Preprocessing_tasks >> Modeling_tasks