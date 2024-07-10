# impressum.py
import streamlit as st

def impressum():
    st.title('Impressum')
    st.write("""
    ### Kontaktinformationen

    **Management Center Innsbruck (MCI)**
    
    Adresse: Universitätsstraße 15, 6020 Innsbruck, Österreich
    Telefon: +43 512 2070-0
    E-Mail: office@mci.edu
    Website: [MCI Website](https://www.mci.edu)

    ### Unser Team

    - **Felicitas Thierbach**
      - E-Mail: tf0261@mci4me.at
    
    - **Svenja Taft**
      - E-Mail: ts7312@mci4me.at
    
    - **Rania Shehata**
      - E-Mail: sr0548@mci4me.at

    ### Haftungsausschluss

    Trotz sorgfältiger inhaltlicher Kontrolle übernehmen wir keine Haftung für die Inhalte externer Links. Für den Inhalt der verlinkten Seiten sind ausschließlich deren Betreiber verantwortlich.
    """)
# Die Funktion impressum() zeigt die Impressumsseite mit Kontaktinformationen und einem Haftungsausschluss an. Auf der Hauptseite des Dashboards wird ein Link zum Impressum angezeigt, der die Benutzer zur Impressumsseite führt.