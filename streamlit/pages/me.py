import streamlit as st
import requests


st.write('page me from streamlit')

token = st.session_state.get("token", None)

if token:
    headers = {'Authorization' :f'Bearer {token}'}

    response = requests.get('http://localhost:1111/users/me', headers = headers )
    st.write(response.status_code)

    st.write('################### from api')
    st.write('name :', response.json()['name'])
    st.write('scope :', response.json()['scope'])
