import os
import pandas as pd
import json
import joblib

def create_folder_if_necessary(output_folderpath, **kwargs):
    # Create folder if necessary
    if not os.path.exists(output_folderpath):
        os.makedirs(output_folderpath)



def get_params_service(params_folder="data/parameters/", 
                       experiment_name="default",
                       service=str, **kwargs):

    with open(params_folder + experiment_name + "_paths.json", 'r') as f:
        params_paths = json.load(f)
    with open(params_folder + experiment_name + "_other.json", 'r') as f:
        params_other = json.load(f)

    params_service = params_paths[service]
    params_service.update(params_other[service])
    scaler = joblib.load(params_folder + experiment_name + "_scaler.pkl")
    classifier = joblib.load(params_folder + experiment_name + "_classifier.pkl")
    params_service.update({"scaler" : scaler})
    params_service.update({"classifier" : classifier})

    return params_service