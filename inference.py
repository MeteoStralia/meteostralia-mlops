# inference.py

import pandas as pd
import joblib
import os
from data_preprocessing import preprocess_data

def load_model(model_path):
    """
    Charger un modèle entraîné depuis un fichier.

    Args:
        model_path (str): Path to the model file.

    Returns:
        model: Loaded model.
    """
    return joblib.load(model_path)

def run_inference(model, data):
    """
    Démarrer l'inférence uilisant le modèle entraîné sur les données d'entrée.

    Args:
        model: Trained model.
        data (pd.DataFrame): Input data.

    Returns:
        pd.Series: Model predictions.
    """
    return model.predict(data)

if __name__ == "__main__":
    # Definir les chemins
    data_path = os.path.join("data", "new_data.csv")
    model_path = os.path.join("models", "random_forest_model.pkl")

    # Charger et effectuer le preprocess des données
    df = pd.read_csv(data_path)
    df = preprocess_data(df)

    # Charger le modèle
    model = load_model(model_path)

    # Démarrer l'inférence
    predictions = run_inference(model, df)
    print(predictions)

