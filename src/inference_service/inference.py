import pandas as pd
import datetime
from src.global_functions import create_folder_if_necessary
import sys
sys.path.append('./src/')
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

if __name__ == "__main__": # TODO mettre en fonction
    # path and parameters
    processed_data_folder = "data/processed_data/" 
    target_column = "RainTomorrow"
    new_data_folder = "data/new_data/" 
    station_ID_path = "data/add_data/station_ID.csv"
    data_to_add_folder = "data/add_data/"
    model_folder = "models/"
    classifier_name = "LogisticRegression"
    predictions_folder = "data/predictions/" 
    timestamp = datetime.datetime.now().timestamp()
    timestamp = str(int(round(timestamp)))

    # predict date
    predict_date = datetime.datetime.today()

    # scrap predict data
    predict_data = scrap_last_predictdata(
        new_data_folder,
        predict_date,
        station_ID_path
    )

    # process scrapped data
    target, features = process_scrapped_data(
        predict_data,
        data_to_add_folder,
        processed_data_folder,
        target_column)
    
    # Load the model
    model = import_model(model_folder,
                         target_column,
                         classifier_name)
    
    # Making predictions
    predictions = model.predict(features)
    predictions = pd.DataFrame(predictions, 
                               index=features.index, 
                               columns=[target_column + "pred"])
    predictions["Date"] = predictions.index.get_level_values(1)
    predictions["Location"] = predictions.index.get_level_values(1)

    # saving predictions
    create_folder_if_necessary(predictions_folder)
    
    predictions.to_csv(predictions_folder + target_column + "_"+timestamp + ".csv")
    

