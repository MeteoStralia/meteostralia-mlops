import os
import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import json
import pandas as pd
from get_predictions_data import get_predictions_data
import plotly.express as px


predictions_path = "../../../data/predictions/"
index_load = ["id_Location", "id_Date"]

df_pred = get_predictions_data(predictions_path, index_load)

df_pred 
# Ajout des coordonnées

cities_coordinates = {
    'Albury': (-36.0734, 146.9169),
    'BadgerysCreek': (-33.8891, 150.7725),
    'Cobar': (-31.8647, 145.8225),
    'CoffsHarbour': (-30.2989, 153.1145),
    'Moree': (-29.4736, 149.8411),
    'Newcastle': (-32.9283, 151.7817),
    'NorahHead': (-33.1920, 151.5216),
    'NorfolkIsland': (-29.0408, 167.9591),
    'Penrith': (-33.7491, 150.6941),
    'Richmond': (-33.5990, 150.7670),
    'Sydney': (-33.8688, 151.2093),
    'SydneyAirport': (-33.9399, 151.1753),
    'WaggaWagga': (-35.1100, 147.3673),
    'Williamtown': (-32.7990, 151.8430),
    'Wollongong': (-34.4278, 150.8931),
    'Canberra': (-35.2809, 149.1300),
    'Tuggeranong': (-35.4135, 149.0705),
    'MountGinini': (-35.4800, 148.9325),
    'Ballarat': (-37.5622, 143.8503),
    'Bendigo': (-36.7580, 144.2805),
    'Sale': (-38.1000, 147.0667),
    'MelbourneAirport': (-37.6733, 144.8431),
    'Melbourne': (-37.8136, 144.9631),
    'Mildura': (-34.1842, 142.1593),
    'Nhil': (-35.6544, 141.6931),
    'Portland': (-38.3553, 141.5883),
    'Watsonia': (-37.7170, 145.1265),
    'Dartmoor': (-37.8689, 141.4203),
    'Brisbane': (-27.4698, 153.0251),
    'Cairns': (-16.9203, 145.7710),
    'GoldCoast': (-28.0167, 153.4000),
    'Townsville': (-19.2589, 146.8184),
    'Adelaide': (-34.9285, 138.6007),
    'MountGambier': (-37.8333, 140.7833),
    'Nuriootpa': (-34.4934, 138.9773),
    'Woomera': (-31.1333, 136.8333),
    'Albany': (-35.0200, 117.8833),
    'Witchcliffe': (-33.7969, 115.1236),
    'PearceRAAF': (-31.8036, 115.9747),
    'PerthAirport': (-31.9385, 115.9773),
    'Perth': (-31.9505, 115.8605),
    'SalmonGums': (-33.0091, 120.3702),
    'Walpole': (-34.9789, 116.6293),
    'Hobart': (-42.8821, 147.3272),
    'Launceston': (-41.4403, 147.1349),
    'AliceSprings': (-23.6980, 133.8807),
    'Darwin': (-12.4634, 130.8456),
    'Katherine': (-14.4683, 132.2615),
    'Uluru': (-25.3444, 131.0369)
}

cities_coordinates["Canberra"][1]

predict_date = datetime.datetime.now() + timedelta(days=-1)

for location in cities_coordinates.keys():
    df_pred.loc[df_pred.Location == location,
                ['Lat']] = cities_coordinates[location][0]
    df_pred.loc[df_pred.Location == location,
                ['Lon']] = cities_coordinates[location][1]


data_plot = df_pred[df_pred.Date == predict_date.strftime('%Y-%m-%d')]
data_plot["RainTomorrowpred"] = data_plot["RainTomorrowpred"].astype(str)
color_rain = {"0" : "yellow", "1" : "blue"}

fig = px.scatter_map(
    data_frame = data_plot, lat = 'Lat', lon = 'Lon',
    hover_name = 'Location',
    hover_data = ['RainTomorrowpred'],
    zoom = 3,
    center = {'lat':-25.3444, 'lon':145},
    width = 1000, height = 750,
    map_style = 'satellite',
    color = "RainTomorrowpred",
    color_discrete_map=color_rain
    
)


fig.update_traces(
    marker = dict(size = 15),
    showlegend = True
)

fig.update_layout(
    
    title = 'Prédictions de pluie par station',
    geo = dict(
        fitbounds='locations',
        center=dict(
            lon=data_plot.Lon.mean(),
            lat=data_plot.Lat.mean()
        ))
)

fig.show()