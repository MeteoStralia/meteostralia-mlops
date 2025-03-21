import pandas as pd
import sys
sys.path.append('../src/')

from src.data_service.ingest_data.scrap_data import scrap_data, format_scrapped_data, save_new_data
from src.data_service.ingest_data.ingest_new_data import reindex_data

new_data_folder = "../data/new_data/"
# set year and month of data
month_scrap = "01"
year_scrap = "2024"
# Locations to request
location_list = ["Canberra","Sydney","Melbourne","Brisbane"]
station_ID = pd.read_csv("../data/add_data/station_ID.csv", sep=";")
# drop bad locations
station_ID = station_ID.dropna(subset = ["Location"])
# drop location without ID
station_ID = station_ID.dropna(subset = ["IDCJDW"])
# convert location ID to string
station_ID["IDCJDW"] = station_ID["IDCJDW"].astype(int).astype(str)
id_list = station_ID.loc[station_ID["Location"].isin(location_list),["IDCJDW"]] 
scrapped_data = pd.DataFrame()
# scrap data for all locations

for location_name in id_list:

    id_location = station_ID.loc[station_ID.Location == location_name,
                                    "IDCJDW"]
    id_location = str(id_location.iloc[0])
    lastdata_location = scrap_data(
        location_name=location_name,
        id_location=id_location,
        year=year_scrap,
        month=month_scrap)
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

# # testing 
# # reading station IDS
# station_ID = pd.read_csv("../../../data/add_data/station_ID.csv", sep=";")
# # drop les stations sans ID
# station_ID = station_ID.dropna(subset = ["IDCJDW"])
# # drop les nouvelles stations pour le moment
# station_ID = station_ID.dropna(subset = ["Location"])
# station_ID["IDCJDW"] = station_ID["IDCJDW"].astype(int).astype(str)

# # Choix de la location puis du mois et de l'année
# location_name = "Perth"
# year = "2025"
# month = "01"
# id_location_test = station_ID.loc[station_ID.Location == location_name,"IDCJDW"]
# id_location_test = str(id_location_test.iloc[0])

# # data save folder
# new_data_folder = "../../../data/new_data/"

# # scrapping
# data_location = scrap_data(location_name, id_location_test, year, month)
# print(data_location)
# # formatting
# data_location = format_scrapped_data(data_location)
# print(data_location)
# # saving
# save_new_data(data_location, new_data_folder)

