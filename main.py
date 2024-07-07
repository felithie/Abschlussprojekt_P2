import streamlit as st
from about_us import about_us
from impressum import impressum
from heart_articles import heart_article
from heart_articles import heart_rate_article
from heart_articles import ekg_article
from heart_articles import vorhofflimmern_article
from heart_articles import herzratenvariabilitaet_article
from anmeldung1 import login, register, personalized_page


# Funktion für die Startseite

def home():
    st.title('Cardio Check')
    st.image('images/herz.jpg')
    st.write("Willkommen bei Cardio Check! Hier können Sie Ihre Herzgesundheit überprüfen und mehr über verschiedene Herzthemen erfahren.")
    st.write("Cardio Check bietet eine Vielzahl von Tools und Informationen zur Überprüfung Ihrer Herzgesundheit. Sie können EKG-Daten analysieren, Ihre Herzfrequenz überwachen und informative Artikel über verschiedene Herzthemen lesen.")
    st.write("Wählen Sie eine der folgenden Optionen aus der Seitenleiste aus, um mehr zu erfahren oder sich anzumelden.")
    st.write("Viel Spaß beim Erkunden von Cardio Check!")
    
# Funktion für Seite 1
def page1():
    about_us()

# Funktion für Seite 2
def page2():
    st.title("Streamlit Anmeldungsseite")
    
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    
    if st.session_state['logged_in']:
        personalized_page.personalized_page()
    else:
        st.sidebar.title("Navigation")
        choice = st.sidebar.radio("Wählen Sie eine Option", ["Anmeldung", "Registrierung"])
        
        if choice == "Anmeldung":
            login()
        elif choice == "Registrierung":
            register()


# Funktion für Seite 3
def page3():
    st.title('Über das Herz')
    st.write('Willkommen auf der Informationsseite über das Herz.')

    st.write("""
    Wähle einen Artikel aus, um mehr zu erfahren:
    """)

    # Artikel-Expander
    with st.expander("Allgemeines zum Herz", expanded=False):
        heart_article()

    with st.expander("Herzfrequenz", expanded=False):
        heart_rate_article()

    with st.expander("Was ist ein EKG?", expanded=False):
        ekg_article()

    with st.expander("Vorhofflimmern", expanded=False):
        vorhofflimmern_article()

    with st.expander("Herzratenvariabilität", expanded=False):
        herzratenvariabilitaet_article()

# Funktion für Seite 4
def page4():
    impressum()

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
st.sidebar.title('Cardio Check')

selection = st.sidebar.radio("Navigation", list(pages.keys()))

# Aktualisiere die Session State basierend auf der Auswahl
st.session_state.page = selection

# Aufrufen der entsprechenden Seiten-Funktion
pages[st.session_state.page]()

