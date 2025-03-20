import pandas as pd
import datetime
import sys
sys.path.append('./src/')
sys.path.append('../') # a virer 
sys.path.append('../../') # à virer

# import needed functions
from data_service.ingest_data.ingest_new_data import load_data, reindex_data
from data_service.ingest_data.scrap_data import scrap_data, format_scrapped_data, save_new_data
from data_service.features.add_features import add_features
from data_service.encode_data.encode_data import encode_data,encode_newdata, trigo_encoder_len, trigo_encoder
from data_service.scale_data.scale_data import scale_dataframe


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
        data_to_add_path="../../data/add_data/",
        data_path = "data/processed_data/",
        target_column = "RainTomorrow"):
    
    # # drop data if target is na
    # predict_data.dropna(subset=target_column)

    # save indexes
    predict_index = predict_data.index

    # add_features
    predict_data = add_features(predict_data,
                                data_to_add_path=data_to_add_path)
    
    data_tmp = pd.read_csv(data_path + "augmented_data.csv")
    # encode data
    predict_data = encode_newdata(
        data_origin=data_tmp,
        new_data=predict_data
        )
    
    # add year and month to predict data
    year = str(predict_data["Date"].dt.year.unique()[0])

    predict_data["Year_" + year] = 1
    predict_data["Month"] = pd.to_datetime(predict_data["Date"]).dt.month
    # encode unique month in sinus and cosinus

    map_month= trigo_encoder("Month").get_mapping(data_tmp)
    map_month= trigo_encoder("Month").get_mapping(data_tmp)
    
    trigo_encoder_len(predict_data["Month"], length=12)

    # splitting in features and target
    target = predict_data[target_column]
    features = predict_data.drop(columns=[target_column])
    target.index = predict_index
    features.index = predict_index

    # drop columns not in current train data
    X_train = load_data(data_path + "X_train_scaled.csv")
    cols_to_drop = features.columns[[x not in X_train.columns for x in features.columns ]]
    features = features.drop(columns=cols_to_drop)

    # drop remaining na features
    features = features.dropna()
    
    # scale features
    features = scale_dataframe(features)

    return target, features

# testing (à vier)
if __name__ == "__main__":
    # Définir les chemins et paramètres
    data_path = "../../data/processed_data/" # à modifier
    target_column = "RainTomorrow"
    new_data_folder = "../../data/new_data/" # à modifier
    station_ID_path = "../../data/add_data/station_ID.csv" # à modifier
    data_to_add_path = "../../data/add_data/" # à modifier
    # predict date
    predict_date = datetime.datetime.today()

    predict_data = scrap_last_predictdata(
        new_data_folder,
        predict_date,
        station_ID_path
    )
    
    target, features = process_scrapped_data(
        predict_data,
        data_to_add_path,
        data_path,
        target_column)


