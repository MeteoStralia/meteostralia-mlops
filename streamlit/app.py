import streamlit as st
import requests
import os
from dotenv import load_dotenv


from pages import navigation

load_dotenv()
api_url = os.getenv('API_URL')

token = st.session_state.get("token", None)

response = requests.get(
        f'http://{api_url}:2222/',
        headers={"Authorization": f"Bearer {token}"}
    )

navigation.header_menu(token, api_url, response)

st.title('Welcome MeteoStralia MLops (from streamlit)')
