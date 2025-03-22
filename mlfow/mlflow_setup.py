import mlflow
import dagshub

from src.data_service.ingest_data.ingest_new_data import load_data, reindex_data
import json
from src.global_functions import create_folder_if_necessary
from src.modeling_service.evaluate.evaluate import evaluate_model
from src.modeling_service.training.train import import_model


mlflow.set_tracking_uri('https://dagshub.com/bruno.vermont/meteostralia-mlops.mlflow')

dagshub.init(repo_owner='bruno.vermont', repo_name='meteostralia-mlops', mlflow=True)

# with mlflow.start_run():

#     # Définir les chemins et paramètres
#     data_path = "data/processed_data/"
#     model_path = "models/"
#     target_column = "RainTomorrow"
#     classifier = "LogisticRegression"
#     metrics_path = "metrics/" + target_column + "/"+classifier
#     create_folder_if_necessary("metrics/" + target_column + "/")
#     # Loading model
#     model = import_model(model_path, target_column, classifier)
#     # Evaluate model and save metrics
#     metrics = evaluate_model(model, data_path, metrics_path)

#     mlflow.