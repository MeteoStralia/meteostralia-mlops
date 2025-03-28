

import pandas as pd
import sys
import os
from sklearn.base import TransformerMixin, ClassifierMixin
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import datetime
import json
import joblib
sys.path.append('./')
# creating parameters
from src.global_functions import create_folder_if_necessary

# indexes
index_load = ["id_Location", "id_Date"]

# Encoding types
vars_binary = ["RainTomorrow", "RainToday"]
vars_dummies = ["Year", "Location", "Climate"] 
vars_ordinal = ['Cloud9am', 'Cloud3pm']
vars_trigo = ["WindGustDir", "WindDir9am", "WindDir3pm", 
              "Month", "Season"]

# threshold for keeping columns (Nas %)
threshold = 0.25

# split parameters
test_size = 0.2
random_state = 1234
sep_method = "classic"         

# scaler
scaler = MinMaxScaler

# model parameters
# classifier_name = "LogisticRegression"
# classifier = LogisticRegression

# model_params = {
#     "class_weight": {0 : 0.3, 1 : 0.7},
#     "C": 1, "max_iter": 500, "penalty": 'l1',
#     "solver": 'liblinear', "n_jobs": -1}
# model_params = {
#     "class_weight": {0 : 1, 1 : 1},
#     "C": 1, "max_iter": 100, "penalty": 'l1',
#     "solver": 'liblinear', "n_jobs": -1}

# testing another classifier       
classifier_name = "RandomForestClassifier"
classifier = RandomForestClassifier
model_params = {
    "class_weight":{0: 0.3, 1: 0.7}, 
    "criterion":"log_loss",
    "max_depth":10,
    "n_estimators":100,
    "n_jobs":-1}

target_column = "RainTomorrow"

# predict date
predict_date = datetime.datetime.today().strftime('%Y-%m-%d')

# Setting experiment parameters
experiment_name = "default"
#run_name = "Logistic_Regression_run2"
run_name = "RandomForest_run_2603"
#artifact_path = "lr_raintomorrow"
artifact_path = "artifact"

# paths and folder
raw_data_path = "data/raw_data/weatherAUS.csv"
current_data_folder = "data/current_data/"
current_data_path = 'data/current_data/current_data.csv'
new_data_folder = 'data/new_data/'
uptodate_data_path = 'data/current_data/uptodate_data.csv'
processed_data_folder = "data/processed_data/"
processed_data_path = 'data/processed_data/nas_completed_data.csv'
data_to_add_folder = "data/add_data/"
augmented_data_path = 'data/processed_data/augmented_data.csv'
encoded_data_path = 'data/processed_data/encoded_data.csv'
metrics_path = "metrics/" + target_column + "/"+classifier_name
station_ID_path = "data/add_data/station_ID.csv"
model_folder = "models/"
predictions_folder = "data/predictions/" 
params_folder = "data/parameters/"

create_folder_if_necessary(params_folder)

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
        params_folder="data/parameters/"):

    
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
            },
        "tracking_service": {"param":""}
    }
    with open(params_folder + "paths_params.json", 'w') as f:
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
                        experiment_name=str,
                        run_name=str,
                        artifact_path=str,
                        params_folder="data/parameters/"):
    
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
            "predict_date": predict_date},
        "tracking_service":{
            "experiment_name": experiment_name,
            "run_name": run_name,
            "artifact_path": artifact_path}
    }
    
    with open(params_folder + "other_params.json", 'w') as f:
        json.dump(params_other, f)

    joblib.dump(scaler, params_folder +  "scaler.pkl")
    joblib.dump(classifier, params_folder + "classifier.pkl")

create_paths_params(
    raw_data_path=raw_data_path,
    current_data_folder=current_data_folder,
    current_data_path=current_data_path,
    new_data_folder=new_data_folder,
    uptodate_data_path=uptodate_data_path,
    processed_data_folder=processed_data_folder,
    processed_data_path=processed_data_path,
    data_to_add_folder=data_to_add_folder,
    augmented_data_path=augmented_data_path,
    encoded_data_path=encoded_data_path,
    model_folder=model_folder,
    metrics_path=metrics_path,
    station_ID_path=station_ID_path,
    predictions_folder=predictions_folder,
    params_folder=params_folder)

create_other_params(
    index_load=index_load,
    vars_binary=vars_binary, 
    vars_dummies=vars_dummies, 
    vars_ordinal=vars_ordinal,
    vars_trigo=vars_trigo,
    threshold=threshold,
    target_column=target_column,
    test_size=test_size,
    random_state=random_state,
    sep_method=sep_method,
    scaler=scaler,
    classifier_name=classifier_name,
    classifier=classifier, 
    model_params=model_params,
    predict_date=predict_date,
    experiment_name=experiment_name,
    run_name=run_name,
    artifact_path=artifact_path,
    params_folder=params_folder)

