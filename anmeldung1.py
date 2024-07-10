import streamlit as st
from database import register_user, get_user, get_user_data
from calculatemaxHR import calculate_hr
from settings_page import user_profile_page

def login():
    """Anmeldeformular für Benutzer."""
    st.subheader("Anmeldung")
    username = st.text_input("Benutzername")
    password = st.text_input("Passwort", type="password")
    if st.button("Anmelden"):
        user = get_user(username)
        if user:  # Wenn der Benutzer gefunden wurde, wird der Benutzername und das Passwort überprüft
            st.write("User found:", user)  # Debug-Ausgabe
        if user and user[2] == password:  # Wenn das Passwort stimmt, wird der Benutzer angemeldet
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success("Erfolgreich angemeldet!")
            st.experimental_rerun()
        else:  # Wenn das Passwort nicht stimmt, wird eine Fehlermeldung ausgegeben
            st.error("Ungültiger Benutzername oder Passwort")

def register():
    """Registrierungsformular um einen neuen Benutzer zu registrieren."""
    st.subheader("Registrierung")
    username = st.text_input("Neuer Benutzername")
    password = st.text_input("Neues Passwort", type="password")
    email = st.text_input("Email")
    name = st.text_input("Name")
    if st.button("Registrieren"):
        try:  # Versucht den Benutzer zu registrieren
            register_user(username, password, email, name)
            st.success("Erfolgreich registriert!")
            st.info("Wechseln Sie zum Anmeldefeld, um sich anzumelden.")
        except ValueError as e:  # Fehlermeldung, wenn der Benutzername bereits existiert
            st.error(f"Fehler bei der Registrierung: {e}")
        except Exception as e:  # Allgemeine Fehlermeldung
            st.error(f"Unerwarteter Fehler bei der Registrierung: {e}")

