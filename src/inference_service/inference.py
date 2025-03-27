import pandas as pd
import datetime
from dotenv import load_dotenv
import sys
import os
sys.path.append('./')
from src.inference_service.scrap_last_data import scrap_last_predictdata, process_scrapped_data
from src.modeling_service.evaluate.evaluate import import_model
from src.global_functions import create_folder_if_necessary, get_params_service

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

def get_predictions_data(predictions_path, index_load = ["id_Location", "id_Date"]):
    predictions_data_files = os.listdir(predictions_path)

    df_pred = pd.DataFrame()

    for file in predictions_data_files:
        pred = pd.read_csv(predictions_path + file, index_col = index_load)
        pred['Location'] = pred.index.get_level_values(0).values
        df_pred = pd.concat([df_pred, pred])
    return df_pred

if __name__ == "__main__": # TODO mettre en fonction
    # path and parameters
    load_dotenv(dotenv_path='src/docker.env')
    params_inference = get_params_service(service="inference_service")
    processed_data_folder = params_inference["processed_data_folder"] 
    target_column = params_inference["target_column"] 
    new_data_folder = params_inference["new_data_folder"] 
    station_ID_path = params_inference["station_ID_path"] 
    data_to_add_folder = params_inference["data_to_add_folder"] 
    model_folder = params_inference["model_folder"] 
    classifier_name = params_inference["classifier_name"] 
    predictions_folder = params_inference["predictions_folder"]

    # predictions save time stamp 
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
    predictions["Location"] = predictions.index.get_level_values(0)

    # saving predictions
    create_folder_if_necessary(predictions_folder)
    
    predictions.to_csv(predictions_folder + "current_prediction" + ".csv")
    all_predictions = get_predictions_data(predictions_folder) 
    all_predictions = all_predictions.drop_duplicates()
    all_predictions.to_csv(predictions_folder + "predict_history_" + target_column + ".csv")



