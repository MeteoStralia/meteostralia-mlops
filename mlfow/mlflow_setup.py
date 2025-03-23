import mlflow
import dagshub

from src.data_service.ingest_data.ingest_new_data import load_data, reindex_data
import json
from src.global_functions import create_folder_if_necessary
from src.modeling_service.evaluate.evaluate import evaluate_model
from src.modeling_service.training.train import import_model
import os

mlflow.set_tracking_uri('https://dagshub.com/bruno.vermont/meteostralia-mlops.mlflow')

dagshub.init(repo_owner='bruno.vermont', repo_name='meteostralia-mlops', mlflow=True)

# # Setting experiment parameters
# experiment_name = "default"
# params_folder = "data/parameters/"
# # Define experiment name, run name and artifact_path name
# apple_experiment = mlflow.set_experiment("Apple_Models")
# run_name = "first_run"
# artifact_path = "rf_apples"

# with mlflow.start_run(run_name=run_name) as run:
# mlflow.log_params(params)
# mlflow.log_metrics(metrics)
# mlflow.sklearn.log_model(
# sk_model=rf, input_example=X_val, artifact_path=artifact_path)
