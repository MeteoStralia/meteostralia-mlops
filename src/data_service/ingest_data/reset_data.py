import sys
sys.path.append('./')
from src.data_service.ingest_data.ingest_new_data import load_data
from src.global_functions import create_folder_if_necessary, get_params_service

def reset_data(raw_data_path="data/raw_data/weatherAUS.csv",
               current_data_folder="data/current_data/", **kwargs):

    # récupère les données raw et les mets dans current
    raw_data = load_data(raw_data_path)
    raw_data.to_csv(current_data_folder + "current_data.csv")

if __name__ == '__main__':
    # # paths and parameters
    # current_data_folder = "data/current_data/"
    # raw_data_path = "data/raw_data/weatherAUS.csv"

    params_data = get_params_service(service="data_service")
    # reset data
    create_folder_if_necessary(params_data["current_data_folder"])
    reset_data(**params_data)
    print("Current data replaced by raw data")