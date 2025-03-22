import sys
sys.path.append('./src/')
from data_service.ingest_data.ingest_new_data import load_data
from global_functions import create_folder_if_necessary

def reset_data(raw_data_path="data/raw_data/weatherAUS.csv",
               current_data_folder="data/current_data/"):

    # récupère les données raw et les mets dans current
    raw_data = load_data(raw_data_path)
    raw_data.to_csv(current_data_folder + "current_data.csv")

if __name__ == '__main__':
    # paths and parameters
    current_data_folder = "data/current_data/"
    raw_data_path = "data/raw_data/weatherAUS.csv"

    # reset data
    create_folder_if_necessary(current_data_folder)
    reset_data(raw_data_path, current_data_folder = current_data_folder)
    print("Current data replaced by raw data")