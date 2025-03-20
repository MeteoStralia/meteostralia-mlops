import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_url = os.getenv('API_URL')



st.write('page_dashboard from streamlit')

token = st.session_state.get("token", None)
headers = {'Authorization' :f'Bearer {token}'}
response = requests.get(f'http://{api_url}:2222/dashboard', headers = headers )


if token:

    st.write(response.status_code)
    st.write('################### from api dashboard.py')

    st.write(response.json())
    # st.write('username :', response.json()['username'])
    # st.write('scope :', response.json()['scope'])

else:
    st.write(response.status_code)
