import streamlit as st

# Funktion für die Startseite
def home():
    st.title('Startseite')
    st.write('Willkommen auf der Startseite!')

# Funktion für Seite 1
def page1():
    st.title('Seite 1')
    st.write('Dies ist die erste Seite.')

# Funktion für Seite 2
def page2():
    st.title('Seite 2')
    st.write('Dies ist die zweite Seite.')

# Funktion für Seite 3
def page3():
    st.title('Seite 3')
    st.write('Dies ist die dritte Seite.')

# Dictionary zur Zuordnung der Seiten
pages = {
    'Startseite': home,
    'Seite 1': page1,
    'Seite 2': page2,
    'Seite 3': page3
}

# Initialisierung der Session State
if 'page' not in st.session_state:
    st.session_state.page = 'Startseite'

# Sidebar mit Seiten-Navigation
st.sidebar.title('Navigation')
if st.sidebar.button('Startseite'):
    selection = 'Startseite'
elif st.sidebar.button('Seite 1'):
    selection = 'Seite 1'
elif st.sidebar.button('Seite 2'):
    selection = 'Seite 2'
elif st.sidebar.button('Seite 3'):
    selection = 'Seite 3'
else:
    selection = 'Startseite'  # Default-Seite

# Button zum Zurückgehen
if st.sidebar.button('Zurück'):
    st.session_state.page = 'Startseite'


# Aufrufen der entsprechenden Seiten-Funktion
pages[st.session_state.page]()
