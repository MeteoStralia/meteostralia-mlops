import os
from dotenv import load_dotenv
from airflow.models import Variable

load_dotenv(dotenv_path='general.env')
load_dotenv(dotenv_path='docker.env')
load_dotenv(dotenv_path='mlflow.env')

Variable.set(key="PROJECTPATH", value=os.environ["PROJECTPATH"])
Variable.update(key="PROJECTPATH", value="PROJECTPATH")
