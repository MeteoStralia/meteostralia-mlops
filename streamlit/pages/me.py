import streamlit as st
import requests


st.write('page me from streamlit')

token = st.session_state.get("token", None)
headers = {'Authorization' :f'Bearer {token}'}
response = requests.get('http://localhost:1111/users/me', headers = headers )


if token:
    st.write(response.status_code)

    st.write('################### from api me.py')
    st.write('name :', response.json()['name'])
    st.write('scope :', response.json()['scope'])
else:
    st.write(response.status_code)
