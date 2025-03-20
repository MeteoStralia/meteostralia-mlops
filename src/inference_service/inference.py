# inference.py

import pandas as pd
import joblib
import os
import datetime
from sklearn.linear_model import LogisticRegression
from global_functions import create_folder_if_necessary

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
    predictions_folder = "../../data/predictions/" 

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
    
    # Charger le modèle
    model = import_model(model_path,
                         target_column,
                         classifier)
    
    predictions=model.predict(features)
    predictions = pd.DataFrame(predictions, index = features.index, columns=[target_column + "pred"])
    predictions["Date"] = predictions.index.get_level_values(1)
    predictions["Location"] = predictions.index.get_level_values(1)

    # saving predictions
    create_folder_if_necessary(predictions_folder)
    timestamp = datetime.datetime.now().timestamp()
    timestamp = str(int(round(timestamp)))
    predictions.to_csv(predictions_folder +target_column+"_"+timestamp + ".csv")
    

