

import pandas as pd
import sys
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LogisticRegression
import datetime

sys.path.append('./src/')

##################
# DATA SERVICE ###
##################

# reset data
raw_data_path = "data/raw_data/weatherAUS.csv"
current_data_folder = "data/current_data/"

# add new data
index = False
current_data_path = 'data/current_data/current_data.csv'
uptodate_data_path = 'data/current_data/uptodate_data.csv'
new_data_folder = 'data/new_data/'

# complete nas
uptodate_data_path = 'data/current_data/uptodate_data.csv'
index = ["id_Location","id_Date"]
processed_data_folder = "data/processed_data/"
processed_data_path = 'data/processed_data/nas_completed_data.csv'
    
# add features
index = ["id_Location","id_Date"]

processed_data_path = 'data/processed_data/nas_completed_data.csv'
data_to_add_folder = "data/add_data/"
augmented_data_path = 'data/processed_data/augmented_data.csv'

# encode data
augmented_data_path = 'data/processed_data/augmented_data.csv'
index = ["id_Location","id_Date"]
vars_binary = ["RainTomorrow", "RainToday"]
vars_dummies = ["Year", "Location", "Climate"] 
vars_ordinal = ['Cloud9am', 'Cloud3pm']
vars_trigo = ["WindGustDir", "WindDir9am", "WindDir3pm", "Month", 
            "Season"]
encoded_data_path = 'data/processed_data/encoded_data.csv'

# split data
encoded_data_path = 'data/processed_data/encoded_data.csv'
index =["id_Location","id_Date"]
threshold = 0.25
target_column = "RainTomorrow"
test_size = 0.2
random_state = 1234
sep_method = "classic"             
processed_data_folder = 'data/processed_data/'

# scale data
processed_data_folder = 'data/processed_data/'
scaler = MinMaxScaler()

######################
# MODELING SERVICE ###
######################

# training
processed_data_folder = "data/processed_data/"
model_params = {
    "class_weight": {0: 0.3, 1: 0.7},
    "C": 1, "max_iter": 500, "penalty": 'l1',
    "solver": 'liblinear', "n_jobs": -1}
classifier = LogisticRegression
model_folder = "models/"
target_column = "RainTomorrow"

# Evaluate
processed_data_folder = "data/processed_data/"
model_folder = "models/"
target_column = "RainTomorrow"
classifier_name = "LogisticRegression"
metrics_path = "metrics/" + target_column + "/"+classifier_name

#######################
# INFERENCE SERVICE ###
#######################

# scrap and process last data

processed_data_folder = "data/processed_data/" 
target_column = "RainTomorrow"
new_data_folder = "data/new_data/" 
station_ID_path = "data/add_data/station_ID.csv"
data_to_add_folder = "data/add_data/"
# predict date
predict_date = datetime.datetime.today()

# inference
model_folder = "models/"
classifier_name = "LogisticRegression"
predictions_folder = "data/predictions/" 
timestamp = datetime.datetime.now().timestamp()
timestamp = str(int(round(timestamp)))
