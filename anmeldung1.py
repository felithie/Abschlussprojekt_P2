import streamlit as st
from user_data import load_user_data, save_user_data
import personalized_page 

def login():
    st.subheader("Anmeldung")
    username = st.text_input("Benutzername")
    password = st.text_input("Passwort", type="password")
    if st.button("Anmelden"):
        users = load_user_data()
        if username in users and users[username]['password'] == password:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success("Erfolgreich angemeldet!")
            st.experimental_rerun()
        else:
            st.error("Ungültiger Benutzername oder Passwort")

def register():
    st.subheader("Registrierung")
    username = st.text_input("Neuer Benutzername")
    password = st.text_input("Neues Passwort", type="password")
    if st.button("Registrieren"):
        users = load_user_data()
        if username not in users:
            users[username] = {'password': password}
            save_user_data(users)
            st.success("Erfolgreich registriert!")
            st.experimental_rerun()
        else:
            st.error("Benutzername bereits vergeben")




