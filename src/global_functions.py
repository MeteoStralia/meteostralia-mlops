import os
import pandas as pd
from sklearn.base import TransformerMixin, ClassifierMixin
import json
import joblib

def create_folder_if_necessary(output_folderpath, **kwargs):
    # Create folder if necessary
    if not os.path.exists(output_folderpath):
        os.makedirs(output_folderpath)


def create_paths_params(
        raw_data_path=str,
        current_data_folder=str,
        current_data_path=str,
        new_data_folder=str,
        uptodate_data_path=str,
        processed_data_folder=str,
        processed_data_path=str,
        data_to_add_folder=str,
        augmented_data_path=str,
        encoded_data_path=str,
        model_folder=str,
        metrics_path=str,
        station_ID_path=str,
        predictions_folder=str,
        params_folder="data/parameters/",
        experiment_name=str):

    
    params_paths = {
        "data_service":{
            "raw_data_path": raw_data_path,
            "current_data_folder": current_data_folder,
            "current_data_path": current_data_path,
            "new_data_folder": new_data_folder,
            "uptodate_data_path": uptodate_data_path,
            "processed_data_folder": processed_data_folder,
            "processed_data_path": processed_data_path,
            "data_to_add_folder": data_to_add_folder,
            "augmented_data_path": augmented_data_path,
            "encoded_data_path": encoded_data_path
            },
        "modeling_service": {
            "processed_data_folder": processed_data_folder,
            "model_folder": model_folder,
            "metrics_path": metrics_path
            },
        "inference_service": {
            "processed_data_folder": processed_data_folder,
            "data_to_add_folder": data_to_add_folder,
            "new_data_folder": new_data_folder,
            "station_ID_path": station_ID_path,
            "model_folder": model_folder,
            "predictions_folder":predictions_folder,
            }
    }
    with open(params_folder + experiment_name + "_paths.json", 'w') as f:
        json.dump(params_paths, f)

def create_other_params(index_load=list(),
                        vars_binary=list(), 
                        vars_dummies=list(), 
                        vars_ordinal=list(),
                        vars_trigo=list(),
                        threshold=float,
                        target_column=str,
                        test_size=float,
                        random_state=int,
                        sep_method=str,
                        scaler=TransformerMixin,
                        classifier_name=str,
                        classifier=ClassifierMixin, 
                        model_params=dict,
                        predict_date=str,
                        params_folder="data/parameters/",
                        experiment_name=str):
    
    params_other = {
        "data_service": {
            "index_load": index_load,
            "vars_binary": vars_binary,
            "vars_dummies": vars_dummies,
            "vars_ordinal": vars_ordinal,
            "vars_trigo": vars_trigo,
            "threshold": threshold,
            "target_column": target_column,
            "test_size": test_size,
            "random_state": random_state,
            "sep_method": sep_method,
            },
        "modeling_service": {
            "classifier_name": classifier_name,
            "model_params": model_params,
            "target_column": target_column},
        "inference_service":{
            "target_column": target_column,
            "classifier_name": classifier_name,
            "predict_date": predict_date}
    }
    
    with open(params_folder + experiment_name + "_other.json", 'w') as f:
        json.dump(params_other, f)

    joblib.dump(scaler, params_folder + experiment_name + "_scaler.pkl")
    joblib.dump(classifier, params_folder + experiment_name + "_classifier.pkl")

def get_params_service(params_folder=os.environ["PARAMS_FOLDER"], 
                       experiment_name=os.environ["EXPERIMENT_NAME"],
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