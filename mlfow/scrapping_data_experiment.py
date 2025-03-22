import pandas as pd
import sys
sys.path.append('../src/')
sys.path.append('../')

from src.data_service.ingest_data.scrap_data import scrap_data, format_scrapped_data, save_new_data
from src.data_service.ingest_data.ingest_new_data import reindex_data

new_data_folder = "../data/new_data/"
# set year and month of data

years_scrap = ["2024","2025"]
months_scrap = {"2024": ["02","05","08","11"],
                "2025": ["01"]}

# Locations to request
location_list = ["Canberra","Sydney","Melbourne","Brisbane"]
station_ID = pd.read_csv("../data/add_data/station_ID.csv", sep=";")
# drop bad locations
station_ID = station_ID.dropna(subset = ["Location"])
# drop location without ID
station_ID = station_ID.dropna(subset = ["IDCJDW"])
# convert location ID to string
station_ID["IDCJDW"] = station_ID["IDCJDW"].astype(int).astype(str)
id_list = station_ID.loc[station_ID["Location"].isin(location_list)] 
scrapped_data = pd.DataFrame()
# scrap data for all locations

for year_scrap in years_scrap:
    for month_scrap in months_scrap[year_scrap]:
        for location_name in location_list:

            id_location = id_list.loc[id_list.Location == location_name,"IDCJDW"]
            id_location = str(id_location.iloc[0])
            data_location = scrap_data(
                location_name=location_name,
                id_location=id_location,
                year=year_scrap,
                month=month_scrap)
            data_location_c = data_location.copy()
            # formatting as raw data
            data_location_c = format_scrapped_data(data_location_c)
            data_location_c = reindex_data(data_location_c)
            # concatenate with all stations data
            scrapped_data = pd.concat([scrapped_data, 
                                                data_location_c])

# copy scrapped data
scrapped_data_c = scrapped_data.copy()

save_data = scrapped_data_c

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

