import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.base import ClassifierMixin 
from sklearn.ensemble import RandomForestClassifier
import joblib
from dotenv import load_dotenv
import sys
sys.path.append('./')
from src.data_service.ingest_data.ingest_new_data import load_data
from src.global_functions import create_folder_if_necessary, get_params_service

def train_model(processed_data_folder="data/processed_data/",
                target_column="RainTomorrow",
                classifier=ClassifierMixin, #TODO find class sklearn
                model_params={},
                model_folder="models/"):
    """
    Entraîner un modèle RandomForest et le sauvegarder sur un fichier.

    Args:
        processed_data_folder (str): Path to the training data CSV file.
        target_column (str): Name of the target column in the data.
        classifier (sklearn classifier class) : Classifier selected
        model_params (dict) : classifier parameters (default {} for default parameters)
        model_folder (str): Path to save the trained model.
    """
    # Loading training data
    X_train = load_data(processed_data_folder + "X_train_scaled.csv")
    y_train = load_data(processed_data_folder + "y_train.csv")
    
    # Entraîner le modèle
    model = classifier(**model_params)
    print("Fitting ", type(model).__name__)
    model.fit(X_train, y_train)

    # save target and model name in model path
    model_path = model_folder+target_column+"/last_run_model.pkl"    # Sauvegarder le modèle
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")
    
if __name__ == "__main__":
    # paths and parameters
    load_dotenv(dotenv_path='src/docker.env')
    params_model = get_params_service(service="modeling_service")
    processed_data_folder = params_model["processed_data_folder"]
    model_params = params_model["model_params"]
    classifier = params_model["classifier"]
    model_folder = params_model["model_folder"]
    target_column = params_model["target_column"]

    # correction for class_weight
    if "class_weight" in model_params.keys():
        copy = model_params["class_weight"].copy()
        for key in model_params["class_weight"].keys():
            copy[int(key)] = copy[key]
            del copy[key]
    
    model_params["class_weight"] = copy

    print(model_params)
    # create models folder
    create_folder_if_necessary(model_folder + target_column +"/")
    # training
    train_model(processed_data_folder, target_column, classifier=classifier, 
                model_params=model_params, model_folder=model_folder)
    
    
