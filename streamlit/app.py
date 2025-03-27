import streamlit as st
import requests
import os
from dotenv import load_dotenv
import emoji

from pages import navigation

load_dotenv()
api_url = os.getenv('API_URL')


st.set_page_config(
    page_title = 'MeteoStralia - MLops',
    page_icon = emoji.emojize('🦘'),
    layout = 'wide',
    initial_sidebar_state = "collapsed"
)

token = st.session_state.get("token", None)

response = requests.get(
        f'http://{api_url}:2222/',
        headers={"Authorization": f"Bearer {token}"}
    )

navigation.header_menu(token, api_url, response)

st.title('Welcome MeteoStralia MLops (from streamlit)')
if token:
    st.write('Bienvenue : ', response.json()['current_user']['username'])
