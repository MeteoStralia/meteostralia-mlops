import os
import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import json
import pandas as pd


predictions_path = "../../../data/predictions/"
index_load = ["id_Location", "id_Date"]

def get_predictions_data(predictions_path, index_load):
    predictions_data_files = os.listdir(predictions_path)

    df_pred = pd.DataFrame()

    for file in predictions_data_files:
        pred = pd.read_csv(predictions_path + file, index_col = index_load)
        pred['Location'] = pred.index.get_level_values(0).values
        df_pred = pd.concat([df_pred, pred])
  
    return df_pred








