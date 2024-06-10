# Funktion für die Anmeldung
import streamlit as st
from user_db_functions import load_user_db, save_user_db


def Anmeldung():
    # Dateipfad für die Benutzerdatenbank
    USER_DB_FILE = 'user_db.json'
    # Initialisierung der Benutzerdatenbank
    users_db = load_user_db(USER_DB_FILE)

    # Initialisierung des session_state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
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
        else:
            st.error("Ungültiger Benutzername oder Passwort.")

    # Weiterleitung basierend auf dem session_state
    if st.session_state.logged_in:
        if st.session_state.page == 'Seite 1':
            Seite1(username)
    
def Seite1(username):
    st.title('Seite 1')
    st.write("Willkommen auf Seite 1!")
    st.write("Hier kannst du neue Auswahlmöglichkeiten implementieren.")

    # Beispiel für Auswahlmöglichkeiten auf Seite 1
    option = st.selectbox("Wähle eine Option", ["Option 1", "Option 2", "Option 3"])

    # Beispiel für Verlinkung zu anderen Seiten basierend auf Auswahl
    if option == "Option 1":
        st.write("Du hast Option 1 ausgewählt.")
    elif option == "Option 2":
        st.write("Du hast Option 2 ausgewählt.")
    elif option == "Option 3":
        st.write("Du hast Option 3 ausgewählt.")


