# about_us.py
import streamlit as st

def about_us(): # Funktion, die die About Us Seite erstellt
    st.title("About Us")
    st.write("""
    Wir sind drei engagierte Studentinnen des Studiengangs Medizin und Sporttechnologie am Management Center Innsbruck (MCI). Unser Team besteht aus:
    
    - **Svenja Taft**
    - **Felicitas Thierbach**
    - **Rania Shehata**
    
    Im Rahmen unseres Programmierübungsunterrichts haben wir diese Website selbst gecodet und gestaltet. Unsere Motivation hinter diesem Projekt war es, unsere Fähigkeiten im Bereich der Programmierung zu verbessern und eine praktische Anwendung zu schaffen, die sowohl unsere technischen Fertigkeiten als auch unser Interesse an Medizin und Sporttechnologie widerspiegelt.""")
    
    # macht 3 Spalten
    col1, col2, col3 = st.columns(3)
    
    # fügt Bilder hinzu
    with col1:
        st.image('images/Bild.Svenja.jpg', caption='Svenja Taft', width=150)
    with col2:
        st.image('images/Bild.Felicitas.jpg', caption='Felicitas Thierbach', width=150)
    with col3:
        st.image('images/Bild.Rania.jpg', caption='Rania Shehata', width=150)
    
    st.write("""Diese Website bietet Ihnen die Möglichkeit, EKG-Daten einzulesen und zu analysieren. Sie können Ihre Herzfrequenzdaten hochladen und diese von unserem System analysieren lassen. Die Ergebnisse der Analyse, wie zum Beispiel die Herzfrequenz, werden grafisch dargestellt, sodass Sie leicht verständliche Einblicke in Ihre Herzgesundheit erhalten.""")
    
    st.write("""Zusätzlich zu den Analysefunktionen bieten wir interessante Miniartikel rund um die Themen Herz, Herzfrequenz und allgemeine kardiologische Gesundheit. Unser Ziel ist es, Ihnen nützliche und leicht verständliche Informationen zu bieten, die Ihnen helfen, mehr über Ihr Herz und dessen Funktionen zu erfahren.""")
    
    st.write("""Vielen Dank, dass Sie unsere Website besuchen. Wir hoffen, dass Sie die Informationen und Funktionen nützlich finden. Wenn Sie Fragen oder Anregungen haben, zögern Sie bitte nicht, uns zu kontaktieren.""")


   
