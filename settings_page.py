import streamlit as st
import pandas as pd
from database import get_user_data, update_user

def user_profile_page():
    # Überprüfen, ob der Benutzer eingeloggt ist
    if 'username' not in st.session_state or not st.session_state['logged_in']:
        st.error("Bitte melden Sie sich zuerst an.")
        return

    # Benutzerdaten für den aktuellen Benutzer abrufen
    user_data = get_user_data(st.session_state['username'])

    # Debug-Ausgabe der geladenen Benutzerdaten
    st.write("Geladene Benutzerdaten:", user_data)

    if user_data:
        age, weight, height, password = user_data
    else:
        age, weight, height, password = 0, 0.0, 0.0, ""

    # Werte initialisieren oder aus session_state laden
    if 'age' not in st.session_state:
        st.session_state['age'] = age
    if 'weight' not in st.session_state:
        st.session_state['weight'] = weight
    if 'height' not in st.session_state:
        st.session_state['height'] = height
    if 'password' not in st.session_state:
        st.session_state['password'] = password

   # st.session_state['current_user'] 
    # Benutzerdaten bearbeiten
    st.subheader("Benutzerdaten bearbeiten")
    st.session_state['username'] = st.text_input("Benutzername", value=st.session_state['username'], disabled=True)
    st.session_state['age'] = st.number_input("Alter", min_value=0, max_value=150, value=st.session_state['age'])
    st.session_state['weight'] = st.number_input("Gewicht (kg)", min_value=0.0, value=st.session_state['weight'])
    st.session_state['height'] = st.number_input("Größe (cm)", min_value=0.0, value=st.session_state['height'])
    
    #st.session_state['password'] = st.text_input("Passwort", type="password", value=st.session_state['password'])

    # Benutzerdaten aktualisieren
    if st.button("Speichern"):
        user_data = [st.session_state['username']  ,st.session_state['age'], st.session_state['weight'], st.session_state['height']] #st.session_state['password']]
        #update_user(st.session_state['username'], st.session_state['age'], st.session_state['weight'], st.session_state['height'], st.session_state['password'])
        st.success("Daten erfolgreich aktualisiert.")

    # Anzeige der gespeicherten Benutzerdaten
    st.subheader("Gespeicherte Benutzerdaten")
    user_data_df = pd.DataFrame([{
        'Benutzername': st.session_state['username'],
        'Alter': st.session_state['age'],
        'Gewicht': st.session_state['weight'],
        'Größe': st.session_state['height'],
        #'Passwort': st.session_state['password']
    }])
    st.table(user_data_df)

    if st.button("Zurück zur Hauptseite"):
        st.session_state['page'] = 'main_page'
        st.experimental_rerun()