import streamlit as st
# from mypersonclass import Person
from mypersonclass import main
import os

def calculatehr_page(selected_person):
    st.title("Herzfrequenz Berechnung")

    # user_id = st.text_input("Geben Sie die Benutzer-ID ein")
    # if user_id:
    #     filename = f"{user_id}.json"

    #     if os.path.exists(filename):
    #         person = Person.load_from_json(filename)
    #         st.success(f"Willkommen zurück, {person.name}!")
    #     else:
    #         name = st.text_input("Geben Sie Ihren Namen ein")
    #         age = st.number_input("Geben Sie Ihr Alter ein", min_value=0, max_value=120, step=1)
    #         gender = st.selectbox("Geben Sie Ihr Geschlecht ein", ["Männlich", "Weiblich", "Andere"])
    #         if st.button("Person erstellen"):
    #             person = Person(name, user_id, age, gender)
    #             person.save_to_json(filename)
    #             st.success("Person wurde erstellt und gespeichert.")

    if not selected_person:
        # implement fehlermeldung
        pass
    else:
        hr = selected_person.calculatemaxhr()
        if hr is not None:
            st.subheader("Berechnete Herzfrequenz")
            st.write(f"Ihre berechnete Herzfrequenz ist: {hr} Schläge pro Minute")
        else:
            st.write("Alter erforderlich für die Berechnung der Herzfrequenz")


#calculatehr_page()