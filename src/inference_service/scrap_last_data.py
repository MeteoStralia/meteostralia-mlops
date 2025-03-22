import pandas as pd
import datetime
import sys
sys.path.append('./src/')
# sys.path.append('../') # a virer 
# sys.path.append('../../') # à virer

# import needed functions
from data_service.ingest_data.ingest_new_data import load_data, reindex_data
from data_service.ingest_data.scrap_data import scrap_data, format_scrapped_data, save_new_data
from data_service.features.add_features import add_features
from data_service.encode_data.encode_data import encode_data,encode_newdata, trigo_encoder_len, trigo_encoder
from data_service.scale_data.scale_data import scale_data


def scrap_last_predictdata(
        new_data_folder = "=data/new_data/",
        predict_date = datetime.datetime.today,
        station_ID_path = "../../data/add_data/station_ID.csv"):
    
    # get previous day date
    predict_date_yesterday = (predict_date + 
                              datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
    
    # get year and month of predict date
    month_predict = predict_date.month
    year_predict = predict_date.year

    # format pour correspondre au site weatherAUS
    if len(str(month_predict)) == 1:
        month_predict = "0" + str(month_predict)
    elif len(str(month_predict)) == 2:
        month_predict = str(month_predict)
    year_predict = str(year_predict)

    predict_date = predict_date.strftime('%Y-%m-%d')

    # Location to request
    station_ID = pd.read_csv(station_ID_path, sep=";")
    # drop bad locations
    station_ID = station_ID.dropna(subset = ["Location"])
    # drop location without ID
    station_ID = station_ID.dropna(subset = ["IDCJDW"])
    # convert location ID to string
    station_ID["IDCJDW"] = station_ID["IDCJDW"].astype(int).astype(str)

    scrapped_data = pd.DataFrame()
    # scrap data for all locations
    for location_name in station_ID["Location"]:

        id_location = station_ID.loc[station_ID.Location == location_name,
                                     "IDCJDW"]
        id_location = str(id_location.iloc[0])
        lastdata_location = scrap_data(
            location_name=location_name,
            id_location=id_location,
            year=year_predict,
            month=month_predict)
        lastdata_location_c = lastdata_location.copy()
        # formatting as raw data
        lastdata_location_c = format_scrapped_data(lastdata_location_c)
        lastdata_location_c = reindex_data(lastdata_location_c)
        # concatenate with all stations data
        scrapped_data = pd.concat([scrapped_data, 
                                          lastdata_location_c])
    
    # copy scrapped data
    scrapped_data_c = scrapped_data.copy()
    
    # print(scrapped_data)
    # keep data only for predict_date and predict date d-1
    predict_data = scrapped_data_c.loc[
        scrapped_data_c["Date"].dt.strftime('%Y-%m-%d').isin([predict_date, predict_date_yesterday])]
    
    # save scrapped data to new_data path to be added in training data (except data for predict_date)
    save_data = scrapped_data_c.loc[
        scrapped_data_c["Date"].dt.strftime('%Y-%m-%d').isin([predict_date, predict_date_yesterday]) == False]
    
    save_new_data(save_data, new_data_folder)
    
    return predict_data

def process_scrapped_data(
        predict_data,
        data_to_add_folder,
        processed_data_folder = "data/processed_data/",
        target_column = "RainTomorrow"):
    
    # # drop data if target is na
    # predict_data.dropna(subset=target_column)

    # save indexes
    predict_index = predict_data.index

    # add_features
    predict_data = add_features(predict_data,
                                data_to_add_folder=data_to_add_folder)
    
    predict_data["Year"] = pd.to_datetime(predict_data["Date"]).dt.year
    predict_data["Month"] = pd.to_datetime(predict_data["Date"]).dt.month
    
    # encode data
    data_tmp = pd.read_csv(processed_data_folder + "augmented_data.csv")
    predict_data = encode_newdata(
        data_origin=data_tmp,
        new_data=predict_data
        )
    
    # encoding for missing years in current data
    if "Year" in predict_data.columns:
        years = predict_data["Year"].unique()
        for year in years :
            predict_data["Year_" + str(year)] = 1
        predict_data=predict_data.drop(columns="Year")

    # splitting in features and target
    target = predict_data[target_column]
    features = predict_data.drop(columns=[target_column])
    target.index = predict_index
    features.index = predict_index

    X_train = load_data(processed_data_folder + "X_train.csv")
    # drop columns not in current train data
    cols_to_drop = features.columns[[x not in X_train.columns for x in features.columns ]]
    features = features.drop(columns=cols_to_drop)

    # drop remaining na features
    features = features.dropna()
    
    # adding missing features
    missing_features = X_train.columns[[x not in features.columns for x in X_train.columns]]
    
    features[missing_features] = 0
    
    # ordering features name
    features = features[X_train.columns]

    # scale features like Xtrain
    X_train_scaled, features = scale_data(X_train=X_train, 
                                          X_test=features)

    return target, features

# testing (à virer)
if __name__ == "__main__":
    # path and parameters
    processed_data_folder = "data/processed_data/" 
    target_column = "RainTomorrow"
    new_data_folder = "data/new_data/" 
    station_ID_path = "data/add_data/station_ID.csv"
    data_to_add_folder = "data/add_data/"

    # predict date
    predict_date = datetime.datetime.today()

    predict_data = scrap_last_predictdata(
        new_data_folder,
        predict_date,
        station_ID_path
    )

    target, features = process_scrapped_data(
        predict_data,
        data_to_add_folder,
        processed_data_folder,
        target_column)


