import os
import pandas as pd
import json
import joblib

def create_folder_if_necessary(output_folderpath, **kwargs):
    # Create folder if necessary
    if not os.path.exists(output_folderpath):
        os.makedirs(output_folderpath)



def get_params_service(params_folder="data/parameters/",
                       service=str, **kwargs):

    with open(params_folder + "paths_params.json", 'r') as f:
        params_paths = json.load(f)
    with open(params_folder + "other_params.json", 'r') as f:
        params_other = json.load(f)

    params_service = params_paths[service]
    params_service.update(params_other[service])
    scaler = joblib.load(params_folder  + "scaler.pkl")
    classifier = joblib.load(params_folder + "classifier.pkl")
    params_service.update({"scaler" : scaler})
    params_service.update({"classifier" : classifier})

    return params_service