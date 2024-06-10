import streamlit as st
from about_us import about_us
from Anmeldung import Anmeldung

# Funktion für die Startseite
def home():
    st.title('Cardio Check')
    st.image('images/herz.jpg')

# Funktion für Seite 1
def page1():
    about_us()

# Funktion für Seite 2
def page2():
    Anmeldung()

# Funktion für Seite 3
def page3():
    st.title('Über das Herz')
    st.write('Dies ist die Informationsseite über das Herz.')

# Funktion für Seite 4
def page4():
    st.title('Impressum')
    st.write('Dies ist die Impressumseite.')

# Dictionary zur Zuordnung der Seiten
pages = {
    'Startseite': home,
    'About Us': page1,
    'Anmeldung': page2,
    'Über das Herz': page3,
    'Impressum': page4
}

# Initialisierung der Session State
if 'page' not in st.session_state:
    st.session_state.page = 'Startseite'

# Sidebar mit Seiten-Navigation
st.sidebar.title('Navigation')
selection = st.sidebar.radio('Navigation', list(pages.keys()))

# Aktualisiere die Session State basierend auf der Auswahl
st.session_state.page = selection

# Aufrufen der entsprechenden Seiten-Funktion
pages[st.session_state.page]()
