import streamlit as st
from database import register_user, get_user

def login():
    st.subheader("Anmeldung")
    username = st.text_input("Benutzername")
    password = st.text_input("Passwort", type="password")
    if st.button("Anmelden"):
        user = get_user(username)
        if user:
            st.write("User found:", user)  # Debug-Ausgabe
        if user and user[2] == password:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success("Erfolgreich angemeldet!")
            st.rerun()
        else:
            st.error("Ungültiger Benutzername oder Passwort")

def register():
    st.subheader("Registrierung")
    username = st.text_input("Neuer Benutzername")
    password = st.text_input("Neues Passwort", type="password")
    email = st.text_input("Email")
    name = st.text_input("Name")
    if st.button("Registrieren"):
        try:
            register_user(username, password, email, name)
            st.success("Erfolgreich registriert!")
            st.rerun()
        except ValueError as e:
            st.error(f"Fehler bei der Registrierung: {e}")
        except Exception as e:
            st.error(f"Unerwarteter Fehler bei der Registrierung: {e}")