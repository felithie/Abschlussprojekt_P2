import os
import streamlit as st
from datetime import datetime
from database import get_user_data, update_user, get_user_id, add_user_file, get_user_files
from database import init_db

init_db() # Initialisierung der Datenbank

def user_profile_page(): # Seite zum Anzeigen und Bearbeiten des Benutzerprofils
    st.subheader("Profileinstellungen")
    
    user_data = get_user_data(st.session_state['username'])
    if user_data:
        age, weight, height, profile_image, firstname, lastname, birth_year, gender = user_data
    else:
        age, weight, height, profile_image, firstname, lastname, birth_year, gender = None, None, None, None, None, None, None, None

    weight = float(weight) if weight is not None else 1.0
    height = float(height) if height is not None else 30.0
    firstname = firstname if firstname is not None else ""
    lastname = lastname if lastname is not None else ""
    birth_year = int(birth_year) if birth_year is not None else 2000
    gender = gender if gender is not None else ""

    current_year = datetime.now().year
    if birth_year:
        age = current_year - birth_year # Berechnung des Alters aus dem Geburtsjahr

    if age == 0 or weight == 0.0 or height == 0.0: # Fehlermeldung, wenn Alter, Gewicht oder Größe nicht gültig sind
        st.error("Bitte aktualisieren Sie Ihr Profil und geben Sie gültige Werte für Alter, Gewicht und Größe an.")

    firstname = st.text_input("Vorname", value=firstname)
    lastname = st.text_input("Nachname", value=lastname)
    birth_year = st.number_input("Geburtsjahr", min_value=1900, max_value=current_year, step=1, value=birth_year)
    gender = st.selectbox("Geschlecht", ["", "Männlich", "Weiblich", "Divers"], index=["", "Männlich", "Weiblich", "Divers"].index(gender))

    age = current_year - birth_year
    st.write(f"Alter: {age} Jahre")
    weight = st.number_input("Gewicht (kg)", min_value=1.0, max_value=300.0, step=0.1, value=weight)
    height = st.number_input("Größe (cm)", min_value=30.0, max_value=300.0, step=0.1, value=height)

    # Bild hochladen
    st.subheader("Profilbild hochladen")
    uploaded_image = st.file_uploader("Wählen Sie ein Bild", type=["jpg", "jpeg", "png"])
    if uploaded_image is not None:
        profile_image = uploaded_image.read()
    
    if st.button("Speichern"):
        if age < 1 or weight < 1.0 or height < 30.0:
            st.error("Bitte geben Sie gültige Werte für Alter, Gewicht und Größe an.")
        else:
            update_user(st.session_state['username'], age, weight, height, profile_image, firstname, lastname, birth_year, gender)
            st.success("Profil aktualisiert!")
            st.experimental_rerun()

    # Profilbild anzeigen
    if profile_image:
        st.subheader("Aktuelles Profilbild")
        st.image(profile_image, width=150)

    # Store the user profile data in session state
    st.session_state['user_profile'] = {
        'name': firstname,
        'lastname': lastname,
        'age': age,
        'gender': gender,
        'weight': weight,
        'height': height
    }
    # Abmelden-Button
    if st.button("Abmelden"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = None
            st.session_state['page'] = 'main_page'
            st.experimental_rerun()

# Aufruf der Benutzerprofilseite
if __name__ == "__main__":
    user_profile_page()
