from user_data import load_user_data, save_user_data
from calculatemaxHR import calculate_hr 
import streamlit as st


# Streamlit-Seitenfunktion zur Berechnung der Herzfrequenz
def calculate_hrpage():
    # Laden der Benutzerdaten
    users = load_user_data()
    # Benutzerdaten für den aktuellen Benutzer abrufen
    user_info = users.get(st.session_state['username'], {})
    # Alter des Benutzers abrufen
    age = user_info.get('age')

    # Falls kein Alter gespeichert ist, Eingabefeld anzeigen
    if age is None:
        age = st.number_input("Alter", min_value=1, max_value=120)
        # Benutzerdaten aktualisieren
        user_info['age'] = age
        users[st.session_state['username']] = user_info
        save_user_data(users)
        
    else:
        st.write(f"Ihr Alter: {age}")
        max_hr = calculate_hr(age)
        st.write(f"Ihre maximale Herzfrequenz: {max_hr}")
    
    if st.button("Zurück zur Hauptseite"):
        st.session_state['page'] = 'main_page'