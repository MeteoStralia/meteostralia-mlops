import streamlit as st
import requests


st.write('page_dashboard from streamlit')



st.write('############ from api')

token = st.session_state.get("token", None)
headers = {'Authorization' :f'Bearer {token}'}
response = requests.get('http://localhost:1111/dashboard', headers = headers )


if token:

    st.write(response.status_code)
    st.write(response.json())
    # st.write('username :', response.json()['username'])
    # st.write('scope :', response.json()['scope'])

else:
    st.write(response.status_code)
