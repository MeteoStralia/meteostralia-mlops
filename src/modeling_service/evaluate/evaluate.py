import os
from dotenv import load_dotenv
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
import mlflow
import dagshub
import joblib
import json
import sys
sys.path.append('./')
#sys.path.append('../../../')
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

    # mflow tracking
    # loading train data to track them as artifacts
    # X_train = load_data(processed_data_folder + "X_train_scaled.csv")
    # y_train = load_data(processed_data_folder + "y_train.csv")
    
    dagshub.auth.add_app_token(os.environ['AIRFLOW_DAGSHUB_USER_TOKEN'], host=None)
    mlflow.set_tracking_uri(os.environ['AIRFLOW_MLFLOW_TRACKING_URI'])
    dagshub.init(url=os.environ['AIRFLOW_MLFLOW_TRACKING_URI'], mlflow=True)
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
    # # paths and parameters
    load_dotenv(dotenv_path='src/docker.env')
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
    # exp = mlflow.get_experiment_by_name(os.environ["EXPERIMENT_NAME"])
    # runs = mlflow.search_runs(experiment_ids=exp.experiment_id)
    
       
