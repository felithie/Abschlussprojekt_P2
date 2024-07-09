import streamlit as st
from database import  get_user_weight, get_user_height

def calulate_bmi(weight, height):
    return weight / (height ** 2)

def display_bmi_info(bmi):
    if bmi < 18.5:
        st.write(f"Ihr BMI: {bmi:.2f} - Untergewicht")
        st.write("Personen mit einem BMI unter 18,5 gelten als untergewichtig. Dies kann auf eine unzureichende Ernährung, Essstörungen oder andere gesundheitliche Probleme hinweisen. Es ist wichtig, einen Arzt oder Ernährungsberater zu konsultieren, um die Ursache des Untergewichts zu ermitteln und geeignete Maßnahmen zur Gewichtszunahme zu ergreifen.")
    elif 18.5 <= bmi < 25:
        st.write(f"Ihr BMI: {bmi:.2f} - Normalgewicht")
        st.write("Ein BMI im Bereich von 18,5 bis 24,9 wird als normal angesehen. Personen in dieser Kategorie haben in der Regel ein geringeres Risiko für gewichtsbedingte Gesundheitsprobleme. Es ist ratsam, eine ausgewogene Ernährung und regelmäßige körperliche Aktivität beizubehalten, um das Normalgewicht zu halten.")
    elif 25 <= bmi < 30:
        st.write(f"Ihr BMI: {bmi:.2f} - Übergewicht")
        st.write("Personen mit einem BMI von 25,0 bis 29,9 gelten als übergewichtig. Übergewicht kann das Risiko für verschiedene gesundheitliche Probleme wie Herzerkrankungen, Bluthochdruck und Diabetes erhöhen. Eine Umstellung der Ernährung und mehr körperliche Aktivität können helfen, das Gewicht zu reduzieren und die Gesundheit zu verbessern. Eine Beratung durch einen Arzt oder Ernährungsberater kann ebenfalls nützlich sein.")
    elif 30 <= bmi < 35:
        st.write(f"Ihr BMI: {bmi:.2f} - Adipositas Grad I")
        st.write("Personen mit einem BMI von 30,0 bis 34,9 gelten als fettleibig (Adipositas Grad I). Fettleibigkeit erhöht das Risiko für schwerwiegende gesundheitliche Probleme wie Herzkrankheiten, Diabetes Typ 2 und bestimmte Krebsarten. Es ist wichtig, einen umfassenden Plan zur Gewichtsreduktion zu erstellen, der eine gesunde Ernährung, regelmäßige Bewegung und möglicherweise medizinische Unterstützung umfasst.")
    elif 35 <= bmi < 40:
        st.write(f"Ihr BMI: {bmi:.2f} - Adipositas Grad II")
        st.write("Personen mit einem BMI von 35,0 bis 39,9 gelten als schwer fettleibig (Adipositas Grad II). Das Risiko für gesundheitliche Probleme ist in dieser Kategorie noch höher. Eine intensive Gewichtsreduktion ist erforderlich. Dies kann eine Kombination aus Ernährungsumstellung, Bewegung und medizinischer Behandlung beinhalten. Eine enge Zusammenarbeit mit einem Arzt oder Spezialisten ist wichtig.")
    else:
        st.write(f"Ihr BMI: {bmi:.2f} - Adipositas Grad III")
        st.write("Personen mit einem BMI von 40,0 oder höher gelten als sehr schwer fettleibig (Adipositas Grad III). Das Risiko für schwerwiegende gesundheitliche Probleme ist in dieser Kategorie sehr hoch. Eine sofortige und intensive Behandlung ist erforderlich. Dies kann medizinische Eingriffe wie eine bariatrische Operation umfassen, zusätzlich zu Ernährungsberatung und regelmäßiger Bewegung. Eine enge Überwachung durch medizinische Fachkräfte ist notwendig.")


def calculateBMI_page():
    st.subheader("BMI berechnen")
    weight = get_user_weight(st.session_state['username'])
    height = get_user_height(st.session_state['username'])
    height_in_meters = height / 100
    if weight is None or height is None:
        st.error("Bitte aktualisieren Sie Ihr Gewicht und Ihre Größe in den Profileinstellungen.")
    else:
        st.write(f"Ihr Gewicht: {weight} kg")
        st.write(f"Ihre Größe: {height_in_meters} m")
        bmi = calulate_bmi(weight, height_in_meters)
        #st.write(f"Ihr BMI: {bmi:.2f}")
        display_bmi_info(bmi)

