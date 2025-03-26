import os
import os
from dotenv import load_dotenv
os.getcwd()

load_dotenv(dotenv_path='general.env')
load_dotenv(dotenv_path='docker.env')
load_dotenv(dotenv_path='mlflow.env')

# # test 
# os.environ['PROJECTPATH']
# os.environ['MLFLOW_TRACKING_USERNAME']
# os.environ['MLFLOW_TRACKING_URI']

# os.environ['EXPERIMENT_NAME']
# os.environ["RUN_NAME"]
# os.environ["ARTIFACT_PATH"] 

from airflow import Variable
Variable.set(key="key", value="value")