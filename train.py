# train.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os
from data_preprocessing import load_data, preprocess_data, split_data

def train_model(data_path, target_column, model_path):
    """
    Entraîner un modèle RandomForest et le sauvegarder sur un fichier.

    Args:
        data_path (str): Path to the input data CSV file.
        target_column (str): Name of the target column in the data.
        model_path (str): Path to save the trained model.
    """
    # Charger et effectuer le preprocess de la donnée
    df = load_data(data_path)
    df = preprocess_data(df)
    X_train, X_test, y_train, y_test = split_data(df, target_column)

    # Entraîner le modèle
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluer le modèle
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy:.2f}")

    # Sauvegarder le modèle
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    # Définir les chemins et paramètres
    data_path = os.path.join("data", "input_data.csv")
    model_path = os.path.join("models", "random_forest_model.pkl")
    target_column = "target"

    # Entraîner le modèle
    train_model(data_path, target_column, model_path)

