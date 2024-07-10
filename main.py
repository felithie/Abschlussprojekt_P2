#main.py 
import streamlit as st
from about_us import about_us
from database import init_db
from impressum import impressum
from heart_articles import heart_article, heart_rate_article, ekg_article, vorhofflimmern_article, herzratenvariabilitaet_article
from anmeldung1 import login, register
from personalized_page import personalized_page

init_db()

# Funktion zur Berechnung des Maximalpulses
def maximalpuls_berechnen(alter, geschlecht):
    if geschlecht.lower() == 'männlich':
        return 220 - alter
    elif geschlecht.lower() == 'weiblich':
        return 226 - alter
    else:
        raise ValueError("Ungültiges Geschlecht. Bitte 'männlich' oder 'weiblich' eingeben.")

# Funktion, um benutzerdefiniertes CSS zu laden
def load_css():
    st.markdown("""
        <style>
            .sidebar .sidebar-content {
                background-color: #333;
                color: #fff;
                font-size: 24px; /* Textgröße in der Sidebar */
            }
            h1, h2, h3, h4, h5, h6 {
                color: #b80f0f;
                font-size: 60px; /* Textgröße der Überschriften */
            }
            p, ol, ul, li, .stButton>button, .stNumberInput input, .stSelectbox, .stExpander .stExpanderHeader {
                font-size: 24px; /* Allgemeine Textgröße */
            }
            .stButton>button {
                background-color: #007bff;
                color: white;
                font-size: 20px; /* Textgröße der Buttons */
            }
            .stButton>button:hover {
                background-color: #0056b3;
                color: white;
            }
        </style>
        """, unsafe_allow_html=True)

# Funktion für die Startseite
def home():
    st.title('Cardio Check')
    st.image('images/herz.jpg')
    st.write("""
    Willkommen bei Cardio Check! Hier können Sie Ihre Herzgesundheit überprüfen und mehr über verschiedene Herzthemen erfahren.
    
    Cardio Check bietet eine Vielzahl von Tools und Informationen zur Überprüfung Ihrer Herzgesundheit. Sie können EKG-Daten analysieren, Ihre Herzfrequenz überwachen, informative Artikel über verschiedene Herzthemen lesen und vieles mehr.
    
    Wählen Sie eine der folgenden Optionen aus der Seitenleiste aus, um mehr zu erfahren oder sich anzumelden.)
    """)
    st.write("""
<span style="color:#b80f0f; font-style:italic;">Viel Spaß beim Erkunden von Cardio Check!</span>
""", unsafe_allow_html=True)

# Funktion für Seite 1
def page1():
    about_us()

# Funktion für Seite 2
def page2():
    st.title("Persönlicher Bereich")

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        personalized_page()
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

    st.write("Wähle einen Artikel aus, um mehr zu erfahren:")

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
    st.title("Trainingspuls- und Maximalpuls-Rechner")

    st.write("""
         Bitte beachten Sie, dass es sich hierbei um Durchschnittswerte handelt.
        Je nach Grundfitness, Tagesform, Veranlagung und externen Faktoren können Ihre tatsächlichen Pulswerte um +/- 10 Schläge/Minute abweichen.
    """)

    alter = st.number_input("Geben Sie Ihr Alter ein:", min_value=1, max_value=120, value=30)
    geschlecht = st.selectbox("Wählen Sie Ihr Geschlecht:", ["männlich", "weiblich"])
    ruhepuls = st.number_input("Geben Sie Ihren Ruhepuls ein:", min_value=30, max_value=150, value=60)

    if st.button("Berechnen"):
        maximalpuls = maximalpuls_berechnen(alter, geschlecht)
        
        st.write(f"### Ihr Maximalpuls (nach Edwards) liegt bei: {maximalpuls} Schlägen pro Minute")
        
        # Tabelle anzeigen
        st.write("""
            ### Ihre individuellen Belastungszonen:
            | Prozent des maximalen Pulses | Belastungszone         | Trainingsbereich                        | Beschreibung |
            |------------------------------|------------------------|----------------------------------------|--------------|
            | 50 - 60 %                    | Gesundheitszone        | Regeneration & Kompensation            | Stärkt das Herz-Kreislauf-System. Hilft bei der Regeneration. Ideal für Anfänger oder für Aufwärm- und Cool-down-Phasen. Sehr geringe Belastung und sehr niedrige Anstrengung. |
            | 60 - 70 %                    | Fettverbrennungszone   | Grundlagen-Ausdauer-Training 1         | Maximale Verbrennung von Kalorien aus Fettreserven. Stärkung des Herz-Kreislauf-Systems. Verbesserung der Grundlagenausdauer, der Erholung und des Stoffwechsels. Ideal für lange Trainingseinheiten während des Basis-Trainings und für Regenerationstraining während der Wettkampfsaison. Geringe Belastung, angenehme Anstrengung. |
            | 70 - 80 %                    | Aerobe Zone            | Grundlagen-Ausdauer-Training 1 bis 2   | Verbesserung von Atmung und Kreislauf. Erhöhung des Trainingstempos und der Trainingseffizienz. Ideal zur Leistungssteigerung und fürs Wettkampftraining. Mittelmäßige Anstrengung, schnelle Atmung. |
            | 80 - 90 %                    | Anaerobe Zone          | Grundlagen-Ausdauer-Training 2         | Enorme Steigerung von Kraft, Geschwindigkeit und Muskelvolumen. Ohne Verwendung von Sauerstoff werden hier Nährstoffe verbrannt. Ideal für erfahrene Sportler, Wettkampftraining. Hohe Anstrengung, Muskelermüdung, schwere Atmung, Laktatbildung. |
            | 90 - 100 %                   | Maximaltraining        | Wettkampf-spezifisches Ausdauer-Training| Maximale Leistungssteigerung. Maximale Beanspruchung von Herz, Kreislauf, Gelenken und Muskeln. Ideal für sehr erfahrene und fitte Sportler, nur kurze Intervalle, Sprinttraining, die letzte Vorbereitung auf kurze Renndistanzen. Maximale Anstrengung, sehr schnelle Muskelermüdung, starkes Brennen in den Muskeln, sehr schwere Atmung, Laktatbildung, Schwindel, manchmal auch Kopfschmerzen oder Übelkeit. Achtung! Erhebliche Gefahr für das Herz bei Freizeitsportlern! Belastung des ganzen Körpers und des Immunsystems schon bei mittellangen Einheiten. |
        """)

# Funktion für Seite 5
def page5():
    impressum()

# Dictionary zur Zuordnung der Seiten
pages = {
    'Startseite': home,
    'About Us': page1,
    'Anmeldung': page2,
    'Über das Herz': page3,
    'Trainingspuls-Rechner': page4,
    'Impressum': page5
}

# Initialisierung der Session State
if 'page' not in st.session_state:
    st.session_state.page = 'Startseite'

# Sidebar mit Seiten-Navigation
st.sidebar.title('Cardio Check')

selection = st.sidebar.radio("Navigation", list(pages.keys()))

# Aktualisiere die Session State basierend auf der Auswahl
st.session_state.page = selection

# Laden des benutzerdefinierten CSS
load_css()

# Aufrufen der entsprechenden Seiten-Funktion
pages[st.session_state.page]()