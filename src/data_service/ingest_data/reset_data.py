import pandas as pd
import sys
sys.path.append('./src/')
from data_service.ingest_data.ingest_new_data import load_data

def reset_data(raw_data_path="data/raw_data/weatherAUS.csv",
               current_data_path = "data/current_data/current_data.csv"):

    # récupère les données raw et les mets dans current
    raw_data = load_data(raw_data_path)
    raw_data.to_csv(current_data_path, index=False)

if __name__ == '__main__':
    reset_data()