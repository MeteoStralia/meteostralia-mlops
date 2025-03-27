from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='.env')

os.environ['AIRFLOW_DOCKER_HOST']