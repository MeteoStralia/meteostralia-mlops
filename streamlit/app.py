import streamlit as st
import requests
import os
from dotenv import load_dotenv
import json
import time

load_dotenv()
api_url = os.getenv('API_URL')


token = st.session_state.get("token", None)


if not token:
    col1, col2 = st.columns(2, vertical_alignment = 'center')

    with col1:

        with st.expander(label = 'login', expanded = False):
            with st.form(key="login_form"):
                username = st.text_input("Nom d'utilisateur")
                password = st.text_input("Mot de passe", type="password")

                login_button = st.form_submit_button(label="login")

                if login_button:
                    data = {'username' : username,
                            'password' : password}

                    response = requests.post(f'http://{api_url}:2222/login', data = data)
                    st.write(response.status_code)

                    if response.status_code == 200:
                        st.session_state["token"] = response.json()["access_token"]
                        st.session_state["authenticated"] = True
                        st.session_state["expander_state"] = False
                        st.switch_page('app.py')

                    else:
                        st.write('acces pas accordé')

    with col2 :

        with st.expander(label = 'sign up', expanded = False):
            with st.form(key = "sign_up_form"):
                email = st.text_input('courriel')
                username = st.text_input("Nom d'utilisateur")
                password = st.text_input("Mot de passe", type = "password")

                sign_up_button = st.form_submit_button(label = "sign up")

                if sign_up_button:
                    data = {
                            'username' : username,
                            'email' : email,
                            'hashed_password' : password}

                    response = requests.post(f'http://{api_url}:2222/sign_up',
                                             headers={'Content-Type': 'application/json'},
                                             data=json.dumps(data)
                                             )

                    if response.status_code == 400:
                        st.write(response.json()['detail'])

                    if response.status_code == 422:
                        st.write(response.json()['detail'][0]['msg'])

                    if response.status_code == 200:
                        data.pop('email')
                        data['password'] = data.pop('hashed_password')
                        st.write(response.json()['message'])
                        time.sleep(2)

                        response = requests.post(f'http://{api_url}:2222/login', data = data)
                        st.session_state["token"] = response.json()["access_token"]
                        st.session_state["authenticated"] = True
                        st.session_state["expander_state"] = False
                        st.switch_page('app.py')


if token:
    logout_button = st.button('logout')

    if logout_button:
        del st.session_state["token"]
        st.session_state["authenticated"] = False
        st.switch_page('app.py')

st.title('Welcome MeteoStralia MLops (from streamlit)')


st.write('########################')

response = requests.get(
        f'http://{api_url}:2222/',
        headers={"Authorization": f"Bearer {token}"}
    )
st.write('Welcome to Meteostralia mlops')

st.write('#######################')

if token:
    st.write(response.json()['message'])

    if response.json()['current_user']['scope'] =='admin':
            col1, col2, col3, col4 = st.columns(4)
    else:
        col1, col2, col3 = st.columns(3)

    with col1 :
        st.page_link(page = 'app.py', label = 'Home', icon = '🏠')

    with col2:
        st.page_link(page = 'pages/prevision.py', label = 'prevision_page', icon = '1️⃣')

    with col3:
        st.page_link(page = 'pages/me.py', label = 'profil_page', icon = '1️⃣')

    if response.json()['current_user']['scope'] == 'admin':
        with col4:
            st.page_link(page = 'pages/dashboard.py', label = 'dashboard', icon = '1️⃣')

else:
    col1, col2 = st.columns(2)

    with col1:
        st.page_link(page = 'app.py', label = 'Home', icon = '🏠')
