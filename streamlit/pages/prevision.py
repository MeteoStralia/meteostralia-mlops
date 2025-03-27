import streamlit as st
import requests
import os
import csv
import time
from dotenv import load_dotenv
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd


from pages.navigation import header_menu


load_dotenv()
api_url = os.getenv('API_URL')

token = st.session_state.get("token", None)

headers = {'Authorization' :f'Bearer {token}'}
response = requests.get(f'http://{api_url}:2222/previsions', headers = headers )

header_menu(token, api_url, response)

st.write('Previsions Page (from streamlit)')
# st.write(response.json())

if token:
    st.write('################### from api prevision.py')
    # st.write(response.status_code)

    df_prev = pd.DataFrame(response.json()['predictions'])
    df_coor = pd.DataFrame(response.json()['coordinates'])
    df_merged = df_prev.merge(df_coor, on = 'location', how = 'left')
    # st.write(df_merged.head())

    color_rain = {"0" : "yellow", "1" : "blue"}

    fig = px.scatter_map(
        data_frame = df_merged, lat = 'lat', lon = 'lon',
        hover_name = 'location',
        hover_data = ['prediction'],
        zoom = 3,
        center = {'lat':-25.3444, 'lon':145},
        width = 1000, height = 750,
        map_style = 'satellite',
        color = "prediction",
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
                # lon=data_plot.Lon.mean(),
                # lat=data_plot.Lat.mean()
            ))
    )

    st.plotly_chart(fig)



else:
    st.warning('you must be connected to acces this page', icon = "⚠️")
    time.sleep(2)
    st.switch_page('app.py')
