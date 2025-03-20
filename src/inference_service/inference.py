# inference.py

import pandas as pd
import joblib
import os
import datetime
from sklearn.linear_model import LogisticRegression


import sys
sys.path.append('./src/')
sys.path.append('../') # a virer 
sys.path.append('../../') # à virer

from scrap_last_data import scrap_last_predictdata, process_scrapped_data
from modeling_service.evaluate.evaluate import import_model

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
    # Définir les chemins et paramètres
    data_path = "../../data/processed_data/" # à modifier
    target_column = "RainTomorrow"
    new_data_folder = "../../data/new_data/" # à modifier
    station_ID_path = "../../data/add_data/station_ID.csv" # à modifier
    data_to_add_path = "../../data/add_data/" # à modifier
    model_path = "../../models/"
    classifier = "LogisticRegression"
    # predict date
    predict_date = datetime.datetime.today()

    # scrap predict data
    predict_data = scrap_last_predictdata(
        new_data_folder,
        predict_date,
        station_ID_path
    )

    # effectuer le preprocess des données
    target, features = process_scrapped_data(
        predict_data,
        data_to_add_path,
        data_path,
        target_column)
    # Definir les chemins
    data_path = os.path.join("data", "new_data.csv")
    

    # Charger le modèle
    model = import_model(model_path,
                         target_column,
                         classifier)
    
    model.predict(features)

    # Démarrer l'inférence
    predictions = run_inference(model, df)
    print(predictions)

