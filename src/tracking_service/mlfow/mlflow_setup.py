import mlflow
import dagshub
import os
# os.environ['MLFLOW_TRACKING_USERNAME'] = "fde7dcd7368ad7d679356e489a202cb0dbbd4464"
# DAGSHUB_USER_TOKEN = "fde7dcd7368ad7d679356e489a202cb0dbbd4464"
# os.environ['MLFLOW_TRACKING_URI'] = "https://dagshub.com/bruno.vermont/meteostralia-mlops.mlflow"

from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import datetime
import sys

sys.path.append('./')
dagshub.auth.add_app_token(os.environ['MLFLOW_TRACKING_USERNAME'], host=None)
mlflow.set_tracking_uri(os.environ['MLFLOW_TRACKING_URI'])
dagshub.init(url=os.environ['MLFLOW_TRACKING_URI'], mlflow=True)

# Setting experiment parameters
experiment_name = "default"
params_folder = "data/parameters/"
#run_name = "Logistic_Regression_run2"
run_name = "RandomForest_run1"
#artifact_path = "lr_raintomorrow"
artifact_path = "rf_raintomorrow"
#mlflow.create_experiment(experiment_name)
# artifact_location = f"s3://"+artifact_path
# mlflow.create_experiment(experiment_name, artifact_location)
# experiment = mlflow.set_experiment(os.environ[experiment_name])

def get_or_create_experiment_id(name):
    exp = mlflow.get_experiment_by_name(name)
    if exp is None:
        exp_id = mlflow.create_experiment(name)
        return exp_id
    return exp.experiment_id

exp_id = get_or_create_experiment_id(experiment_name)
exp = mlflow.set_experiment(experiment_name)

# Setting mlflow env for other container

f = open("src/docker.env", "w")
f.write("EXPERIMENT_NAME="+experiment_name+"\n")
f.write("PARAMS_FOLDER="+params_folder+"\n")
f.write("RUN_NAME="+run_name+"\n")
f.write("ARTIFACT_PATH="+artifact_path+"\n")
f.flush()

# Setting default parameters
os.environ["EXPERIMENT_NAME"] = experiment_name
os.environ["PARAMS_FOLDER"] = params_folder

#artifact_location = f"s3://{s3-bucket-name}/mlruns"

