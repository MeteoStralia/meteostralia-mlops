

import pandas as pd
import sys
import os
from sklearn.base import TransformerMixin, ClassifierMixin
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
import datetime
import json
import joblib

sys.path.append('./src/')
sys.path.append('./')

# Setting default parameters
experiment_name = "default"
os.environ["EXPERIMENT_NAME"] = experiment_name
params_folder = "data/parameters/"
os.environ["PARAMS_FOLDER"] = params_folder

from src.global_functions import create_folder_if_necessary, create_paths_params, create_other_params, get_params_service

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
classifier_name = "LogisticRegression"
classifier = LogisticRegression

model_params = {
    "class_weight": {0 : 0.3, 1 : 0.7},
    "C": 1, "max_iter": 500, "penalty": 'l1',
    "solver": 'liblinear', "n_jobs": -1}
target_column = "RainTomorrow"

# predict date
predict_date = datetime.datetime.today().strftime('%Y-%m-%d')

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


# creating parameters json files

create_folder_if_necessary(params_folder)

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
    params_folder=params_folder,
    experiment_name=experiment_name)

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
    params_folder=params_folder,
    experiment_name=experiment_name)

# # testing
# params_data = get_params_service(
#     params_folder=params_folder,
#     experiment_name=experiment_name,
#     service="data_service")
# params_modeling = get_params_service(
#     params_folder=params_folder,
#     experiment_name=experiment_name,
#     service="modeling_service")
# params_inference = get_params_service(
#     params_folder=params_folder,
#     experiment_name=experiment_name,
#     service="inference_service")

# print(params_data)