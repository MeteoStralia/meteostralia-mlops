import mlflow
import dagshub
import os
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import datetime
import sys

sys.path.append('./')
from src.global_functions import get_params_service
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')

dagshub.auth.add_app_token(os.environ['AIRFLOW_DAGSHUB_USER_TOKEN'], host=None)
mlflow.set_tracking_uri(os.environ['AIRFLOW_MLFLOW_TRACKING_URI'])
dagshub.init(url=os.environ['AIRFLOW_MLFLOW_TRACKING_URI'], mlflow=True)

params_tracking = get_params_service(service="tracking_service")

def get_or_create_experiment_id(name):
    exp = mlflow.get_experiment_by_name(name)
    if exp is None:
        exp_id = mlflow.create_experiment(name)
        return exp_id
    return exp.experiment_id


# Setting experiment parameters
experiment_name = params_tracking["experiment_name"]
run_name = params_tracking["run_name"]
artifact_path = params_tracking["artifact_path"]

exp_id = get_or_create_experiment_id(experiment_name)
exp = mlflow.set_experiment(experiment_name)

# Setting mlflow env for other container

f = open("src/docker.env", "w")
f.write("EXPERIMENT_NAME="+experiment_name+"\n")
f.write("EXPERIMENT_ID="+exp_id+"\n")
f.write("RUN_NAME="+run_name+"\n")
f.write("ARTIFACT_PATH="+artifact_path+"\n")
f.flush()

