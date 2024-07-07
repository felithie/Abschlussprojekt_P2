# Funktion für die Anmeldung
import streamlit as st
from user_db_functions import load_user_db, save_user_db
import os
import calculatedhr_page
import mypersonclass

def Anmeldung():
    # Dateipfad für die Benutzerdatenbank
    USER_DB_FILE = 'user_db.json'
    # Initialisierung der Benutzerdatenbank
    users_db = load_user_db(USER_DB_FILE)

    # Initialisierung des session_state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'page' not in st.session_state:
        st.session_state.page = 'Anmeldung'
    
    st.title('Anmeldung')

    # Benutzername und Passwortfelder
    username = st.text_input("Benutzername")
    password = st.text_input("Passwort", type='password')

    # Registrierung
    if st.button("Registrieren"):
        if username in users_db:
            st.error("Benutzername bereits vergeben.")
        else:
            users_db[username] = {'password': password ,'page': 'Seite 1'}
            save_user_db(users_db)
            st.success("Registrierung erfolgreich!")
            st.session_state.logged_in = True
            st.session_state.page = 'Seite 1'  # Weiterleitung nach Registrierung
            
    # Anmeldung
    if st.button("Anmelden"):
        if username in users_db:
            if users_db[username]['password'] == password:
                st.success("Anmeldung erfolgreich!")
                st.session_state.logged_in = True
                st.session_state.page = users_db[username]['page']  # Weiterleitung nach Anmeldung
                # selected_person = mypersonclass.Person()
                
        else:
            st.error("Ungültiger Benutzername oder Passwort.")
            


