import pandas as pd
import numpy as np
import sys
from dotenv import load_dotenv
sys.path.append('./')
from src.data_service.ingest_data.ingest_new_data import load_data, reindex_data
from src.global_functions import get_params_service

def get_season_AU(x):

    if (x.month, x.day) < (3, 20) or (x.month, x.day) > (12, 20):
        return 'Summer'
    elif (x.month, x.day) < (6, 21):
        return 'Autumn'
    elif (x.month, x.day) < (9, 20):
        return 'Winter'
    elif (x.month, x.day) <= (12, 20):
        return 'Spring'
    else:
        raise IndexError("Invalid Input")

# TODO : Ajouter des variables lags / rolling mean

def add_features(df, data_to_add_folder="data/add_data/"):
    # Ajout de la variable Season
    df_return = df.copy()
    df_return["Season"] = pd.to_datetime(df_return["Date"]).apply(lambda x: get_season_AU(x))
    # Ajout de la variable climate
    Location_climate = pd.read_csv(data_to_add_folder +"Location_Climate.csv")
    df_return = pd.merge(df_return, Location_climate,  on="Location", how="left")
    return df_return

if __name__ == '__main__':
    # paths and parameters
    load_dotenv(dotenv_path='src/docker.env')
    params_data = get_params_service(service="data_service")
    processed_data_path = params_data['processed_data_path']
    data_to_add_folder = params_data["data_to_add_folder"]
    index_load = params_data["index_load"]
    augmented_data_path = params_data['augmented_data_path']

    # load data 
    df = load_data(processed_data_path, index=index_load)
    df_augmented = add_features(df, data_to_add_folder)
    df_augmented = reindex_data(df_augmented)

    # save all data to process data
    df_augmented.to_csv(augmented_data_path, index=True)
    print("Augmented data saved to ", augmented_data_path)
    print("New features :", df_augmented.columns[[x not in df.columns for x in df_augmented.columns]].to_list())

