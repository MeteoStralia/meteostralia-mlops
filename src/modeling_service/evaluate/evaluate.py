# train.py
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
import joblib
import sys
sys.path.append('./src/')
from data_service.ingest_data.ingest_new_data import load_data
import json
from global_functions import create_folder_if_necessary

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
       "class 0 recall":recall_score(y_test, y_pred, pos_label=0)
    }

    # Saving metrics to json file
    save_metrics(metrics_path, metrics)
    print(f"metrics saved to {metrics_path}")

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
    processed_data_folder = "data/processed_data/"
    model_folder = "models/"
    target_column = "RainTomorrow"
    classifier_name = "LogisticRegression"
    metrics_path = "metrics/" + target_column + "/"+classifier_name
    create_folder_if_necessary("metrics/" + target_column + "/")
    # Loading model
    model = import_model(model_folder, target_column, classifier_name)
    # Evaluate model and save metrics
    evaluate_model(model, processed_data_folder, metrics_path)
