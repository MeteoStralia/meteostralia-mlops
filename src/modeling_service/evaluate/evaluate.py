import os
# A SUPPRIMER
# experiment_name = "default"
# os.environ["EXPERIMENT_NAME"] = experiment_name
# params_folder = "data/parameters/"
# os.environ["PARAMS_FOLDER"] = params_folder
# run_name = "Logistic_Regression_run"
# os.environ["RUN_NAME"] = run_name
# artifact_path = "lr_raintomorrow"
# os.environ["ARTIFACT_PATH"] = artifact_path
# os.environ['MLFLOW_TRACKING_USERNAME'] = "fde7dcd7368ad7d679356e489a202cb0dbbd4464"
# DAGSHUB_USER_TOKEN = "fde7dcd7368ad7d679356e489a202cb0dbbd4464"
# os.environ['MLFLOW_TRACKING_URI'] = "https://dagshub.com/bruno.vermont/meteostralia-mlops.mlflow"

from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
import mlflow
import dagshub
import joblib
import json
import sys

sys.path.append('./')
from src.data_service.ingest_data.ingest_new_data import load_data
from src.global_functions import create_folder_if_necessary, get_params_service

def evaluate_model(
        model,
        processed_data_folder="data/processed_data/",
        metrics_path="metrics/"):
    """
    Entraîner un modèle RandomForest et le sauvegarder sur un fichier.

    Args:
        model: trained model to evaluate
        processed_data_folder (str): Path to the test data CSV file.
        metrics_path (str): Path to save the metrics (json)
    """

    # loading test data
    X_test = load_data(processed_data_folder + "X_test_scaled.csv")
    y_test = load_data(processed_data_folder + "y_test.csv")
    
    # Evaluer le modèle
    y_pred = model.predict(X_test)

    metrics = {
       "accuracy": accuracy_score(y_test, y_pred),
       "f1_score": f1_score(y_test, y_pred, pos_label=1),
       "class 1 precision": precision_score(y_test, y_pred, pos_label=1),
       "class 1 recall":recall_score(y_test, y_pred, pos_label=1),
       "class 0 precision": precision_score(y_test, y_pred, pos_label=0),
       "class 0 recall":recall_score(y_test, y_pred, pos_label=0),
       "roc_auc_score":roc_auc_score(y_test, y_pred)
    }

    # Saving metrics to json file
    save_metrics(metrics_path, metrics)
    print(f"metrics saved to {metrics_path}")

    #mflow tracking
    dagshub.auth.add_app_token(os.environ['MLFLOW_TRACKING_USERNAME'], host=None)
    mlflow.set_tracking_uri(os.environ['MLFLOW_TRACKING_URI'])
    dagshub.init(url=os.environ['MLFLOW_TRACKING_URI'], mlflow=True)
    mlflow.set_experiment(os.environ["EXPERIMENT_NAME"])
    with mlflow.start_run(run_name=os.environ["RUN_NAME"]) as run:
        mlflow.log_metrics(metrics)
        mlflow.log_params(model.get_params())
        mlflow.sklearn.log_model(
            sk_model=model, input_example=X_test,
              artifact_path=os.environ["ARTIFACT_PATH"])
        
    return metrics


def save_metrics(metrics_path, metrics):
    metrics_path = metrics_path + "_metrics.json"
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f)

def import_model(
        model_folder="models/",
        target_column="RainTomorrow",
        classifier_name="LogisticRegression"):
    """
    Load a saved model

    Args:
        model_path (str): Folder where the model is stored.
        target_column (str): Name of the target column in the data.
        classifier (str) : Name of selected classifier 
    
    Returns:
        model : sklearn trained model
    """
    # Load the model
    model_path = model_folder+target_column+"/"+classifier_name+".pkl"    
    model = joblib.load(model_path)
    return model

if __name__ == "__main__":
    # paths and parameters
    params_model = get_params_service(service="modeling_service")
    processed_data_folder = params_model["processed_data_folder"]
    model_folder = params_model["model_folder"]
    target_column = params_model["target_column"]
    classifier_name = params_model["classifier_name"]
    metrics_path = params_model["metrics_path"]

    create_folder_if_necessary("metrics/" + target_column + "/")
    # Loading model
    model = import_model(model_folder, target_column, classifier_name)
    # Evaluate model and save metrics
    evaluate_model(model, processed_data_folder, metrics_path)
