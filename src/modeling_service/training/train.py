# train.py

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
import sys
sys.path.append('./src/')
from data_service.ingest_data.ingest_new_data import load_data, reindex_data
#from data_preprocessing import load_data, preprocess_data, split_data


def train_model(data_path="data/processed_data/",
                target_column="RainTomorrow",
                classifier=LogisticRegression,
                model_params={},
                model_path="models/"):
    """
    Entraîner un modèle RandomForest et le sauvegarder sur un fichier.

    Args:
        data_path (str): Path to the training data CSV file.
        target_column (str): Name of the target column in the data.
        classifier (sklearn classifier class) : Classifier selected
        model_params (dict) : classifier parameters (default {} for default parameters)
        model_path (str): Path to save the trained model.
    """
    # Loading training data
    X_train = load_data(data_path + "X_train_scaled.csv")
    y_train = load_data(data_path + "y_train.csv")

    # Entraîner le modèle
    model = classifier(**model_params)
    model.fit(X_train, y_train)

    # save target and model name in model path
    model_path = model_path+target_column+"/"+type(model).__name__+".pkl"    # Sauvegarder le modèle
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    # Définir les chemins et paramètres
    data_path = "data/processed_data/"
    model_params = {
        "class_weight": {0: 0.3, 1: 0.7},
        "C": 1, "max_iter": 500, "penalty": 'l1',
        "solver": 'liblinear', "n_jobs": -1}
    classifier = LogisticRegression
    model_path = "models/"
    target_column = "RainTomorrow"

    # Entraîner le modèle
    train_model(data_path, target_column, classifier, model_params, model_path, )
