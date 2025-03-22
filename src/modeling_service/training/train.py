# train.py

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.base import ClassifierMixin 
from sklearn.ensemble import RandomForestClassifier
import joblib
import sys
sys.path.append('./src/')
from data_service.ingest_data.ingest_new_data import load_data
from global_functions import create_folder_if_necessary

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
    model_path = model_folder+target_column+"/"+type(model).__name__+".pkl"    # Sauvegarder le modèle
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")


if __name__ == "__main__":
    # paths and parameters
    processed_data_folder = "data/processed_data/"
    model_params = {
        "class_weight": {0: 0.3, 1: 0.7},
        "C": 1, "max_iter": 500, "penalty": 'l1',
        "solver": 'liblinear', "n_jobs": -1}
    classifier = LogisticRegression
    model_folder = "models/"
    target_column = "RainTomorrow"

    # create models folder
    create_folder_if_necessary(model_folder + target_column +"/")
    # training
    train_model(processed_data_folder, target_column, classifier=classifier, 
                model_params=model_params, model_folder=model_folder)
