import pandas as pd
import numpy as np
# TODO régler les paths pour inclure les fonctions d'autres modules
import sys
sys.path.append('./src/')
sys.path.append('../') # a virer 
sys.path.append('../../') # à virer
sys.path.append('../../data/') # à virer
from data_service.ingest_data.ingest_new_data import load_data, reindex_data

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

def add_features(df, data_to_add_path = "data/add_data/"):
    # Ajout de la variable Season
    df["Season"] = pd.to_datetime(df["Date"]).apply(lambda x: get_season_AU(x))
    # Ajout de la variable climate
    Location_climate = pd.read_csv(data_to_add_path +"Location_Climate.csv")
    df = pd.merge(df, Location_climate,  on="Location", how="left")
    return df

if __name__ == '__main__':
    # load data 
    process_data_path = 'data/processed_data/nas_completed_data.csv'
    df = load_data(process_data_path, index =["id_Location","id_Date"])
    df = add_features(df)
    df = reindex_data(df)
    # save all data to process data
    process_data_path = 'data/processed_data/augmented_data.csv'
    df.to_csv(process_data_path, index = True)

