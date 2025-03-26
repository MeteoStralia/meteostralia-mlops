import os
import os
from airflow.models import Variable
from dotenv import load_dotenv
os.getcwd()

load_dotenv(dotenv_path='general.env')
load_dotenv(dotenv_path='mlflow.env')

# # test 
# os.environ['PROJECTPATH']
# os.environ['MLFLOW_TRACKING_USERNAME']
# os.environ['MLFLOW_TRACKING_URI']


Variable.set("PROJECTPATH") = os.getcwd()
Variable.set("MLFLOW_TRACKING_USERNAME") = os.environ["MLFLOW_TRACKING_USERNAME"]
Variable.set("MLFLOW_TRACKING_URI") = os.environ["MLFLOW_TRACKING_URI"]

# test
Variable.set(key="PROJECTPATH")
