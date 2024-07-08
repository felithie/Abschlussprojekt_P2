import streamlit as st
from database import get_user_data
from calculatemaxHR import calculate_hr
from settings_page import user_profile_page
# Streamlit-Seitenfunktion zur Berechnung der Herzfrequenz
def calculate_hrpage():
    # Laden der Benutzerdaten
    #user_data = get_user_data(st.session_state['username'])
    age = user_profile_page()

    # Alter aus den gespeicherten Benutzerdaten verwenden
    if age is None:
      st.error("Bitte aktualisieren Sie Ihr Alter in den Profileinstellungen.")
    else:
        st.write(f"Ihr Alter: {age}")
        max_hr = calculate_hr(age)
        st.write(f"Ihre maximale Herzfrequenz: {max_hr}")   

    #    st.write(f"Ihr Alter: {age}")
    #    max_hr = calculate_hr(age)
    #    st.write(f"Ihre maximale Herzfrequenz: {max_hr}")
    
    if st.button("Zurück zur Hauptseite"):
        st.session_state['page'] = 'main_page'
        st.experimental_rerun()