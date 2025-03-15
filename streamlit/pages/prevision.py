import streamlit as st
import requests



st.write('Previsions Page (from streamlit)')





st.write('################################################')

response = requests.get(url = 'http://localhost:1111/previsions')
st.write(response.json())
st.write('status_code :', response.status_code)

st.write('#############################################')
