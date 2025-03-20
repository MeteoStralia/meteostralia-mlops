import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_url = os.getenv('API_URL')



token = st.session_state.get("token", None)



# header de la page d'accueil
col1, col2 = st.columns([5, 2], vertical_alignment = 'center')

with col1:
    st.title('Welcome MeteoStralia MLops (from streamlit)')

with col2:

    if not token:
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

    if token:
        logout_button = st.button('logout')

        if logout_button:
            del st.session_state["token"]
            st.session_state["authenticated"] = False
            st.switch_page('app.py')



st.write('########################')

response = requests.get(
        f'http://{api_url}:2222/',
        headers={"Authorization": f"Bearer {token}"}  # Ajout du token dans l'en-tête Authorization
    )
st.write('Welcome to Meteostralia mlops')
# st.write(response.json())

st.write('#######################')


#accessibilité des boutons en fonction de la connection
if token:
    if response.json()['scope'] =='admin':
            col1, col2, col3, col4 = st.columns(4)
    else:
        col1, col2, col3 = st.columns(3)

    with col1 :
        st.page_link(page = 'app.py', label = 'Home', icon = '🏠')

    with col2:
        st.page_link(page = 'pages/prevision.py', label = 'prevision_page', icon = '1️⃣')

    with col3:
        st.page_link(page = 'pages/me.py', label = 'profil_page', icon = '1️⃣')

    if response.json()['scope'] == 'admin':
        with col4:
            st.page_link(page = 'pages/dashboard.py', label = 'dashboard', icon = '1️⃣')

else:
    col1, col2 = st.columns(2)

    with col1:
        st.page_link(page = 'app.py', label = 'Home', icon = '🏠')
