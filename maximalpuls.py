import streamlit as st

def maximalpuls_berechnen(alter, geschlecht):
    if geschlecht.lower() == 'männlich':
        return 220 - alter
    elif geschlecht.lower() == 'weiblich':
        return 226 - alter
    else:
        raise ValueError("Ungültiges Geschlecht. Bitte 'm' für männlich oder 'w' für weiblich eingeben.")

# Streamlit Setup
st.title("Trainingspuls- und Maximalpuls-Rechner")
st.write("""
    ### Bitte beachte, dass es sich hierbei um Durchschnittswerte handelt.
    Je nach Grundfitness, Tagesform, Veranlagung und externen Faktoren können deine tatsächlichen Pulswerte um +/- 10 Schläge/Minute abweichen.
""")

alter = st.number_input("Gib dein Alter ein:", min_value=1, max_value=120, value=30)
geschlecht = st.selectbox("Wähle dein Geschlecht:", ["männlich", "weiblich"])
ruhepuls = st.number_input("Gib deinen Ruhepuls ein:", min_value=30, max_value=150, value=60)

if st.button("Berechne"):
    maximalpuls = maximalpuls_berechnen(alter, geschlecht)
    
    st.write(f"### Dein Maximalpuls (nach Edwards) liegt bei: {maximalpuls} Schlägen pro Minute")
    
    # Tabelle anzeigen
    st.write("""
        ### Deine individuellen Belastungszonen:
        | Prozent deines maximalen Pulses | Belastungszone        | Trainingsbereich                      | Beschreibung |
        |---------------------------------|-----------------------|---------------------------------------|--------------|
        | 50 - 60 %                       | Gesundheitszone       | Regeneration & Kompensation           | Stärkt das Herz-Kreislauf-System. Hilft bei der Regeneration. Ideal für Anfänger oder für Aufwärm- und Cool-down-Phasen. Sehr geringe Belastung und sehr niedrige Anstrengung. |
        | 60 - 70 %                       | Fettverbrennungszone  | Grundlagen-Ausdauer-Training 1        | Maximale Verbrennung von Kalorien aus Fettreserven. Stärkung des Herz-Kreislauf-Systems. Verbesserung der Grundlagenausdauer, der Erholung und des Stoffwechsels. Ideal für lange Trainingseinheiten während des Basis-Trainings und für Regenerationstraining während der Wettkampfsaison. Geringe Belastung, angenehme Anstrengung. |
        | 70 - 80 %                       | Aerobe Zone           | Grundlagen-Ausdauer-Training 1 bis 2  | Verbesserung von Atmung und Kreislauf. Erhöhung des Trainingstempos und der Trainingseffizienz. Ideal zur Leistungssteigerung und fürs Wettkampftraining. Mittelmäßige Anstrengung, schnelle Atmung. |
        | 80 - 90 %                       | Anaerobe Zone         | Grundlagen-Ausdauer-Training 2        | Enorme Steigerung von Kraft, Geschwindigkeit und Muskelvolumen. Ohne Verwendung von Sauerstoff werden hier Nährstoffe verbrannt. Ideal für erfahrene Sportler, Wettkampftraining. Hohe Anstrengung, Muskelermüdung, schwere Atmung, Laktatbildung. |
        | 90 - 100 %                      | Maximaltraining       | Wettkampf-spezifisches Ausdauer-Training | Maximale Leistungssteigerung. Maximale Beanspruchung von Herz, Kreislauf, Gelenken und Muskeln. Ideal für sehr erfahrene und fitte Sportler, nur kurze Intervalle, Sprinttraining, die letzte Vorbereitung auf kurze Renndistanzen. Maximale Anstrengung, sehr schnelle Muskelermüdung, starkes Brennen in den Muskeln, sehr schwere Atmung, Laktatbildung, Schwindel, manchmal auch Kopfschmerzen oder Übelkeit. Achtung! Erhebliche Gefahr für das Herz bei Freizeitsportlern! Belastung des ganzen Körpers und des Immunsystems schon bei mittellangen Einheiten. |
    """)