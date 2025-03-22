import pandas as pd
import numpy as np

import sys
sys.path.append('../')
sys.path.append('../src/')

from src.global_functions import create_folder_if_necessary
from src.data_service.ingest_data.reset_data import reset_data
from src.data_service.ingest_data.ingest_new_data import load_data, reindex_data, add_data
from src.data_service.complete_nas.complete_nas import create_pipeline_nas
from src.data_service.features.add_features import add_features
from src.data_service.encode_data.encode_data import encode_data, encode_newdata
from src.data_service.split_data.split_data import split_data
from src.data_service.scale_data.scale_data import scale_data
from src.modeling_service.training.train import train_model
from src.modeling_service.evaluate.evaluate import import_model, evaluate_model
from src.inference_service.inference import run_inference
from src.inference_service.scrap_last_data import scrap_last_predictdata, process_scrapped_data
import params

##################
# DATA SERVICE ###
##################

# 1) reset data
create_folder_if_necessary(current_data_folder)
reset_data(current_data_folder = current_data_folder)
print("Current data replaced by raw data")

# 2) add new data

# load current data
df_current = load_data(current_data_path)
df_current = reindex_data(df_current)
# list data files in new data folder
new_data_files = os.listdir(new_data_folder)
# add new data to current data
for file in new_data_files:
    df_current = add_data(new_data_folder + file, df_current)

# drop columns not needed
df_current = df_current.drop(columns='Unnamed: 0')
df_current = df_current.drop(columns = ['id_Location', 'id_Date'])

# save all data to current data and uptodate data
df_current.reset_index().to_csv(current_data_path, index = False)
print("new data saved to current")
df_current.to_csv(uptodate_data_path, index = True)
print("new data saved to uptodate")

# 3) complete nas
# load current data

df_uptodate = load_data(current_data_path, 
                        index =["id_Location","id_Date"])
                        *
# add year and month (TODO add this in load data or before)
df_uptodate["Year"] = pd.to_datetime(df_uptodate["Date"]).dt.year
df_uptodate["Month"] = pd.to_datetime(df_uptodate["Date"]).dt.month

# changing cloud to string (this variable is an index) (TODO add this in load data or before)
df_uptodate["Cloud3pm"] = df_uptodate["Cloud3pm"].astype(str).replace('nan',np.nan)
df_uptodate["Cloud9am"] = df_uptodate["Cloud9am"].astype(str).replace('nan',np.nan)

# create Nas completion pipeline
complete_nas_pipeline = create_pipeline_nas()

# check Nas before 
nas_before = pd.DataFrame(df_uptodate.isna().sum())

# apply pipeline
df_uptodate = complete_nas_pipeline.fit_transform(df_uptodate)

# print Nas after
nas_after = pd.DataFrame(df_uptodate.isna().sum())
nas_after = pd.merge(nas_before, nas_after, left_index=True, right_index=True)
nas_after.columns = ['Avant', 'Après']
print(nas_after)

# save all data to process data
create_folder_if_necessary(process_data_folder)
df_uptodate.to_csv(process_data_path, index=True)
print("Completed data saved to ", process_data_path)

# 4) add features

# load data 
df = load_data(process_data_path, index =["id_Location","id_Date"])
df_augmented = add_features(df)
df_augmented = reindex_data(df_augmented)
# save all data to process data
df_augmented.to_csv(augmented_data_path, index = True)
print("Augmented data saved to ", augmented_data_path)
print("New features :", df_augmented.columns[[x not in df.columns for x in df_augmented.columns]].to_list())

# 5) encode data
# load data 
augmented_data_path = 'data/processed_data/augmented_data.csv'
df = load_data(augmented_data_path, index =["id_Location","id_Date"])
df = encode_data(data_to_encode=df)
# save all data to process data
df.to_csv(encoded_data_path, index=True)
print("Encoded data saved to ", encoded_data_path)

# 6) split data
# load data 
df = load_data(encoded_data_path, index =["id_Location","id_Date"])
# drop na (TODO : add a dropna function)
missing_percentages = df.isna().mean()
# Colonnes à conserver
columns_to_keep = missing_percentages[missing_percentages <= threshold].index
columns_dropped = missing_percentages[missing_percentages > threshold].index
df = df[columns_to_keep]
df = df.dropna()
df = df.drop(columns = "Date")

X_train, X_test, y_train, y_test = \
    split_data(df, target_column = "RainTomorrow", 
                test_size=0.2, random_state=1234,
                sep_method="classic")
                                                
# save all data to process data
X_train.to_csv(process_data_folder + "X_train.csv", index=False)
X_test.to_csv(process_data_folder + "X_test.csv", index=False)
y_train.to_csv(process_data_folder + "y_train.csv", index=False)
y_test.to_csv(process_data_folder + "y_test.csv", index=False)
print("Training and test data saved to ", process_data_folder)

# 7) scale data

# load data 
X_train = load_data(process_data_folder + "X_train.csv")
X_test = load_data(process_data_folder + "X_test.csv")
X_train_scaled, X_test_scaled = scale_data(X_train, X_test, scaler=MinMaxScaler())                                           
# save all data to process data
X_train_scaled.to_csv(process_data_folder + "X_train_scaled.csv", index=False)
X_test_scaled.to_csv(process_data_folder + "X_test_scaled.csv", index=False)
print("Scaled training and test features saved to ", process_data_folder)

######################
# MODELING SERVICE ###
######################

# 1) training
create_folder_if_necessary(model_folder + target_column +"/")
# Entraîner le modèle
train_model(processed_data_folder, target_column, classifier, 
            model_params, model_folder)


# 2) Evaluate
create_folder_if_necessary("metrics/" + target_column + "/")
# Loading model
model = import_model(model_folder, target_column, classifier_name)
# Evaluate model and save metrics
evaluate_model(model, processed_data_folder, metrics_path)

#######################
# INFERENCE SERVICE ###
#######################

# 1) scrap last data

# scrap predict data
predict_data = scrap_last_predictdata(
    new_data_folder,
    predict_date,
    station_ID_path
)

# process scrapped data
target, features = process_scrapped_data(
    predict_data,
    data_to_add_path,
    processed_data_folder,
    target_column)

# 2) inference

# Load the model
model = import_model(model_folder,
                        target_column,
                        classifier_name)

# Making predictions
predictions=model.predict(features)
predictions = pd.DataFrame(predictions, 
                            index=features.index, 
                            columns=[target_column + "pred"])
predictions["Date"] = predictions.index.get_level_values(1)
predictions["Location"] = predictions.index.get_level_values(1)

# saving predictions
create_folder_if_necessary(predictions_folder)
timestamp = datetime.datetime.now().timestamp()
timestamp = str(int(round(timestamp)))
predictions.to_csv(predictions_folder +target_column+"_"+timestamp + ".csv")




