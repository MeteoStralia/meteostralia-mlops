import streamlit as st
import requests
import os
import emoji
from dotenv import load_dotenv

from pages.navigation import header_menu

load_dotenv()
api_url = os.getenv('API_URL')

st.set_page_config(
    page_title = 'MeteoStralia - MLops',
    page_icon = emoji.emojize('🦘'),
    layout = 'wide',
    initial_sidebar_state = "collapsed"
)



token = st.session_state.get("token", None)

headers = {'Authorization' :f'Bearer {token}'}
response = requests.get(f'http://{api_url}:2222/dashboard', headers = headers )

header_menu(token, api_url, response)

st.write('page_dashboard from streamlit')


if token:

    st.write(response.status_code)
    st.write('################### from api dashboard.py')

    st.write(response.json())
    # st.write('username :', response.json()['username'])
    # st.write('scope :', response.json()['scope'])

else:
    st.write(response.status_code)
