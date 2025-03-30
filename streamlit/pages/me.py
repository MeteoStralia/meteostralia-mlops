import streamlit as st
import requests
import os
from dotenv import load_dotenv
import time
import emoji

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
response = requests.get(f'http://{api_url}:2222/users/me', headers = headers )

header_menu(token, api_url, response)

st.write('page me from streamlit')

if token:
    col1, col2 = st.columns([3, 2], vertical_alignment = 'center')

    with col1:
        st.write('################### from api me.py')
        info_user = response.json()['current_user']

        st.write('Username : ', info_user['username'])
        st.write('Email : ', info_user['email'])
        st.write('Privilège : ', info_user['username'])
        st.write('Password : this is top secret')

    with col2:

        delete_account_button = st.button('supprimer le compte')

        if delete_account_button:

            if response.json()['current_user']['username'] == 'admin':
                st.write('opération impossible')
            else:
                response = requests.delete(f'http://{api_url}:2222/disable_user', headers = headers )
                if response.status_code == 200:
                    st.write(response.json())
                    time.sleep(2)

                    del st.session_state["token"]
                    st.session_state["authenticated"] = False
                    st.switch_page('app.py')

else:
    st.warning('you must be connected to acces this page', icon = "⚠️")
    with st.spinner('you will be redirected to homepage'):
        time.sleep(2)
    st.switch_page('app.py')
