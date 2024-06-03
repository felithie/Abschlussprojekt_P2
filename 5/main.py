import streamlit as st
import read_person_data
import ekgdata
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from person import Person
import numpy as np
import os

def callback():
    print(f"The user has changed to{st.session_state.aktuelle_versuchsperson} and {st.session_state.aktuelles_ekg}")

# Zu Beginn

# Lade alle Personen
person_names = read_person_data.get_person_list(read_person_data.load_person_data())

# Anlegen diverser Session States
## Gewählte Versuchsperson
if 'aktuelle_versuchsperson' not in st.session_state:
    st.session_state.aktuelle_versuchsperson = 'None'

## Anlegen des Session State. Bild, wenn es kein Bild gibt
if 'picture_path' not in st.session_state:
    st.session_state.picture_path = 'data/pictures/none.jpg'

## Session State für Pfad zu EKG Daten 
if 'ekg_path' not in st.session_state:
    st.session_state.ekg_path = None

# Design des Dashboards

# Schreibe die Überschrift
st.write("# EKG APP")
st.write("## Versuchsperson auswählen")

# Auswahlbox, wenn Personen anzulegen sind
st.session_state.aktuelle_versuchsperson = st.selectbox(
    'Versuchsperson',
    options = person_names, key="select_versuchsperson")

# Name der Versuchsperson
st.write("Der Name ist: ", st.session_state.aktuelle_versuchsperson)

# Date input slot
current_person_dict = read_person_data.find_person_data_by_name(st.session_state.aktuelle_versuchsperson)

current_person = Person(current_person_dict)

ekg_tests = current_person_dict["ekg_tests"]
ekg_dates = [ekg["date"] for ekg in ekg_tests]

st.write("## Datum auswählen")
st.session_state.aktuelles_ekg = st.selectbox(
    'EKG-Datum',
    options = ekg_dates, key="sbEKGDatum",
    on_change=callback)
selected_ekg = [ekg for ekg in ekg_tests if ekg["date"] == st.session_state.aktuelles_ekg][0]


st.write("Das ausgewählte Datum ist:", st.session_state.aktuelles_ekg)

# create a new EKGdata object
current_ekg = ekgdata.EKGdata(selected_ekg)
st.session_state.ekg_path = current_ekg.data

# TODO: Weitere Daten wie Geburtsdatum etc. schön anzeigen

# Nachdem eine Versuchsperson ausgewählt wurde, die auch in der Datenbank ist
# Finde den Pfad zur Bilddatei

if os.path.exists(st.session_state.ekg_path):
    st.write("EKG-Daten vorhanden")
else:
    st.write("EKG-Daten nicht vorhanden")

st.write("Name der Versuchsperson: ", current_person.firstname, current_person.lastname, ":sunglasses:")
st.write("Geburtsjahr: ", current_person.date_of_birth)
st.write("Alter: ", current_person.age)
st.write("Maximale Herzfrequenz :anatomical_heart: : ", current_person.calc_max_heart_rate())


if st.session_state.aktuelle_versuchsperson in person_names:
    person_data = read_person_data.find_person_data_by_name(st.session_state.aktuelle_versuchsperson)
    st.session_state.picture_path = person_data.get("picture_path", 'data/pictures/none.jpg')
    st.session_state.ekg_path = person_data.get("ekg_path", 'data/ekg_data/01_Ruhe.txt')  # Use .get to handle missing keys

# Bild anzeigen
image = Image.open(st.session_state.picture_path)
st.image(image, caption=st.session_state.aktuelle_versuchsperson)

# Öffne EKG-Daten
# TODO: Für eine Person gibt es ggf. mehrere EKG-Daten. Diese müssen über den Pfad ausgewählt werden können
# Vergleiche Bild und Person
if st.session_state.ekg_path is not None:

    # Lade die EKG-Daten im df
    df = pd.read_csv(st.session_state.ekg_path, sep='\t', header=None, names=['EKG in mV', 'Time in ms'])
    df["Time in s"] = df["Time in ms"] / 1000  # Convert milliseconds to seconds

    # Detect the peaks
    peaks = ekgdata.EKGdata.find_peaks(df["EKG in mV"].copy(), 340, 5)

    # EKG-Daten als Matplotlib Plot anzeigen
    # Nachdem die EKG, Daten geladen wurden
    # Erstelle den Plot als Attribut des Objektes
    fig = ekgdata.EKGdata.make_ekg_plot(peaks, df)
    # Zeige den Plot an
    st.plotly_chart(fig)

    # Plot the heart rate
    heart_rate_times, heart_rate_at_peaks = ekgdata.EKGdata.estimate_hr(peaks)

    #print(heart_rate_times)
    #print('---')
    #print(current_ekg)


    fig2 = ekgdata.EKGdata.make_hf_plot(heart_rate_times, heart_rate_at_peaks)
    st.plotly_chart(fig2)


else:
    st.write("Keine EKG-Daten vorhanden.")
