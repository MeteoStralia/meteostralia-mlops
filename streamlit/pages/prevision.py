import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_url = os.getenv('API_URL')



st.write('Previsions Page (from streamlit)')

token = st.session_state.get("token", None)
headers = {'Authorization' :f'Bearer {token}'}
response = requests.get(f'http://{api_url}:2222/previsions', headers = headers )


if token:
    st.write(response.status_code)

    st.write('################### from api prevision.py')
    st.write('name :', response.json()['name'])
    st.write('scope :', response.json()['scope'])
else:
    st.write(response.status_code)
