import streamlit as st
import requests
import time
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

    # st.write(response.status_code)
    st.write('################### from api dashboard.py')

    # st.write(response.json())

    col1, col2, col3 = st.columns(3)

    with col1:
        st.page_link('http://localhost:9090/graph?g0.expr=api_request_home_total&g0.tab=0&g0.stacked=0&g0.show_exemplars=0&g0.range_input=5m',
                    label = 'Prometheus',
                    icon = '📊')

    with col2:
        st.page_link('http://localhost:8080/home',
                     label = 'Airflow',
                     icon = '📊')
    # st.write('username :', response.json()['username'])
    # st.write('scope :', response.json()['scope'])

else:
    st.warning('you must be connected to acces this page', icon = "⚠️")
    time.sleep(2)
    st.switch_page('app.py')
