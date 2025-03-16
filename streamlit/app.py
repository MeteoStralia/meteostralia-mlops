import streamlit as st
import requests


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

                    response = requests.post('http://localhost:1111/login', data = data)
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

response = requests.get('http://localhost:1111/')
st.write(response.json())
st.write('status_code :', response.status_code)

st.write('#######################')

token = st.session_state.get("token", None)


#accessibilité des boutons en fonction de la connection
if token:
    col1, col2, col3= st.columns(3)

    with col1 :
        st.page_link(page = 'app.py', label = 'Home', icon = '🏠')

    with col2:
        st.page_link(page = 'pages/prevision.py', label = 'prevision_page', icon = '1️⃣')

    with col3:
        st.page_link(page = 'pages/me.py', label = 'profil_page', icon = '1️⃣')

else:
    col1, col2 = st.columns(2)

    with col1:
        st.page_link(page = 'app.py', label = 'Home', icon = '🏠')
