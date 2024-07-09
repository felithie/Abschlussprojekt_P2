#settings_page.py
import os
import streamlit as st
from database import get_user_data, update_user, get_user_id, add_user_file, get_user_files

def user_profile_page():
    st.subheader("Profileinstellungen")
    
    user_data = get_user_data(st.session_state['username'])
    if user_data:
        age, weight, height = user_data
    else:
        age, weight, height = 0, 0, 0

    age = int(age) if age is not None else 0
    weight = float(weight) if weight is not None else 0.0
    height = float(height) if height is not None else 0.0

    age = st.number_input("Alter", min_value=0, max_value=120, step=1, value=age)
    weight = st.number_input("Gewicht (kg)", min_value=0.0, max_value=300.0, step=0.1, value=weight)
    height = st.number_input("Größe (cm)", min_value=0.0, max_value=300.0, step=0.1, value=height)

    if st.button("Speichern"):
        update_user(st.session_state['username'], age, weight, height)
        st.success("Profil aktualisiert!")
        st.experimental_rerun()

    st.subheader("EKG Dateien hochladen")
    uploaded_file = st.file_uploader("Wählen Sie eine Datei", type=["csv"])
    if uploaded_file is not None:
        user_id = get_user_id(st.session_state['username'])
        if user_id is not None:
            # Erstellen Sie das Verzeichnis, falls es nicht existiert
            uploads_dir = "uploads"
            if not os.path.exists(uploads_dir):
                os.makedirs(uploads_dir)

            file_path = os.path.join(uploads_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            add_user_file(user_id, file_path)
            st.success(f"Datei {uploaded_file.name} hochgeladen und gespeichert!")

    st.subheader("Hochgeladene Dateien")
    user_id = get_user_id(st.session_state['username'])
    if user_id is not None:
        files = get_user_files(user_id)
        for file in files:
            st.write(file)

