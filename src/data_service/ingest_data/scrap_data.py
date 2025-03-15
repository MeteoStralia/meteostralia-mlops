import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime

# TODO : à containeriser avec arguments en entrée (location name, year, month)
# TODO : permettre d'envoyer une liste de location et de dates...

def scrap_data(location_name = str, id_location = str, year = str, month = str):
    """
    scrap data on https://reg.bom.gov.au/climate for a location a year and a month

    Args:
        location_name (str): location name.
        id_location (str): location id (see data/add_data/station_ID.csv).
        year (str) : requested data  year
        month (str) : requested data month ("01", "02", ... ,"12")
    Returns:
        pd.DataFrame: raw scrapped DataFrame.
    """

    url_csv = "https://reg.bom.gov.au/climate/dwo/" + \
        year + month + "/text/IDCJDW" + str(id_location) + \
              "." + year + month + ".csv"
    
    response = requests.get(url_csv)
    
    if response.status_code == 200:
        
        soup = BeautifulSoup(response.content, "html.parser")
        lines = soup.prettify().split('\n')
        
        for line in range(len(lines)) :
            if lines[line][2:6] == "Date":
                skiprows = line-1
                print(skiprows)  
                break
        
        datatmp = pd.read_csv(url_csv, skiprows= skiprows, index_col=0, encoding = "ISO-8859-1")
        
        if datatmp.columns[0] == "Date":
            datatmp["Location"] = location_name
            datatmp.index = range(1,data_location.shape[0]+1)
            return datatmp

def format_scrapped_data(data_to_format):
    """
    format scrapped data from https://reg.bom.gov.au/climate to raw data format

    Args:
        data_to_format : DataFrame to format
    Returns:
        pd.DataFrame: formatted DataFrame.
    """


    dico_rename = {
        'Minimum temperature (°C)' : 'MinTemp',
        'Maximum temperature (°C)' : 'MaxTemp',
        'Rainfall (mm)' : 'Rainfall',
        'Evaporation (mm)' : 'Evaporation',
        'Sunshine (hours)' : 'Sunshine',
        'Direction of maximum wind gust ' : 'WindGustDir',
        'Speed of maximum wind gust (km/h)' : 'WindGustSpeed',
        '9am Temperature (°C)' : 'Temp9am',
        '9am relative humidity (%)' : 'Humidity9am',
        '9am cloud amount (oktas)' : 'Cloud9am',
        '9am wind direction' : 'WindDir9am',
        '9am wind speed (km/h)' : 'WindSpeed9am',
        '9am MSL pressure (hPa)' : 'Pressure9am',
        '3pm Temperature (°C)' : 'Temp3pm',
        '3pm relative humidity (%)' : 'Humidity3pm',
        '3pm cloud amount (oktas)' : 'Cloud3pm',
        '3pm wind direction' : 'WindDir3pm',
        '3pm wind speed (km/h)' : 'WindSpeed3pm',
        '3pm MSL pressure (hPa)' : 'Pressure3pm',
        }
    
    data_to_format.rename(columns = dico_rename, inplace = True)
    data_to_format.drop(columns = ['Time of maximum wind gust'], inplace = True)
    data_to_format['RainToday'] = data_to_format['Rainfall'].apply(lambda x: 'Yes' if x >= 1 else 'No')
    data_to_format['RainTomorrow'] = data_to_format['RainToday'].shift(-1)
    data_to_format['Humidity3pm'] = data_to_format['Humidity3pm'].astype(float)
    data_to_format['WindSpeed3pm'] = data_to_format['WindSpeed3pm'].apply(lambda x : 0 if x == 'Calm' else x)
    data_to_format['WindSpeed9am'] = data_to_format['WindSpeed9am'].apply(lambda x : 0 if x == 'Calm' else x)
    data_to_format['Humidity3pm'] = data_to_format['Humidity3pm'].astype(float)
    data_to_format['Humidity9am'] = data_to_format['Humidity9am'].astype(float)
    data_to_format['WindSpeed3pm'] = data_to_format['WindSpeed3pm'].astype(float)
    data_to_format['WindSpeed9am'] = data_to_format['WindSpeed9am'].astype(float)
    data_to_format['WindDir9am'] = data_to_format['WindDir9am'].replace(' ', pd.NA)
    data_to_format['WindDir9am'] = data_to_format['WindDir9am'].ffill()
    data_to_format['WindDir3pm'] = data_to_format['WindDir3pm'].replace(' ', pd.NA)
    data_to_format['WindDir3pm'] = data_to_format['WindDir3pm'].ffill()

    return data_to_format

def save_new_data(data_to_save, file_folder):
    """
    Save formatted data to file folder with a timestamp (in seconds)

    Args:
        data_to_save : DataFrame to save
        file_folder : folder where the data is saved
    """

    timestamp = datetime.datetime.now().timestamp()
    timestamp = str(int(round(timestamp)))
    data_to_save.to_csv(file_folder + "weatherAU_scrapdata_" + timestamp + ".csv")


# # testing 
# # reading station IDS
# station_ID = pd.read_csv("../../../data/add_data/station_ID.csv", sep=",")
# # drop les stations sans ID
# station_ID = station_ID.dropna(subset = ["IDCJDW"])
# # drop les nouvelles stations pour le moment
# station_ID = station_ID.dropna(subset = ["Location"])
# station_ID["IDCJDW"] = station_ID["IDCJDW"].astype(int).astype(str)

# # Choix de la location puis du mois et de l'année
# location_name = "Sydney"
# year = "2025"
# month = "02"
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