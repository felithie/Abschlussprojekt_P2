#calculatemaxHRpage.py
import streamlit as st
from database import get_user_age
from calculatemaxHR import calculate_hr

def calculate_hrpage():
    st.subheader("Maximale Herzfrequenz berechnen")
    age = get_user_age(st.session_state['username'])
# Alter aus den gespeicherten Benutzerdaten verwenden und maximale Herzfrequenz berechnen

    if age is None:
        st.error("Bitte aktualisieren Sie Ihr Alter in den Profileinstellungen.") # Fehlermeldung, wenn das Alter nicht gefunden wurde
    else:
        st.write(f"Ihr Alter: {age}")
        max_hr = calculate_hr(age)
        st.write(f"Ihre maximale Herzfrequenz: {max_hr}")   # Ausgabe der maximalen Herzfrequenz

    



