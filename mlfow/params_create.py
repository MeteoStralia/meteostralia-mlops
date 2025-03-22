

import pandas as pd
import sys
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LogisticRegression
import datetime

sys.path.append('./src/')

##################
# DATA SERVICE ###
##################

# paths and folder
raw_data_path = "data/raw_data/weatherAUS.csv"
current_data_folder = "data/current_data/"
current_data_path = 'data/current_data/current_data.csv'
new_data_folder = 'data/new_data/'
uptodate_data_path = 'data/current_data/uptodate_data.csv'
process_data_folder = "data/processed_data/"
process_data_path = 'data/processed_data/nas_completed_data.csv'
data_to_add_folder = "data/add_data/"
augmented_data_path = 'data/processed_data/augmented_data.csv'
encoded_data_path = 'data/processed_data/encoded_data.csv'

# indexes 
index_load = ["id_Location","id_Date"]

# Encoding types
vars_binary = ["RainTomorrow", "RainToday"]
vars_dummies = ["Year", "Location", "Climate"] 
vars_ordinal = ['Cloud9am', 'Cloud3pm']
vars_trigo = ["WindGustDir", "WindDir9am", "WindDir3pm", "Month", 
            "Season"]

# threshold for keeping columns (Nas %)
threshold = 0.25

# split parameters
target_column = "RainTomorrow"
test_size = 0.2
random_state = 1234
sep_method = "classic"         

# scaler
scaler = MinMaxScaler()

######################
# MODELING SERVICE ###
######################

# model parameters
classifier_name = "LogisticRegression"
classifier = LogisticRegression
model_params = {
    "class_weight": {0: 0.3, 1: 0.7},
    "C": 1, "max_iter": 500, "penalty": 'l1',
    "solver": 'liblinear', "n_jobs": -1}
target_column = "RainTomorrow"

# paths and folder
processed_data_folder = "data/processed_data/"
model_folder = "models/"
metrics_path = "metrics/" + target_column + "/"+ classifier_name

#######################
# INFERENCE SERVICE ###
#######################

# paths and folder
processed_data_folder = "data/processed_data/" 
new_data_folder = "data/new_data/" 
station_ID_path = "data/add_data/station_ID.csv"
model_folder = "models/"
predictions_folder = "data/predictions/" 
data_to_add_path = "data/add_data/"

# model parameters
target_column = "RainTomorrow"
classifier_name = "LogisticRegression"
# predict date
predict_date = datetime.datetime.today()





