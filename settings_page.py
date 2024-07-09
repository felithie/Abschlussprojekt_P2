#settings_page.py
import streamlit as st
from database import get_user_data, update_user

def user_profile_page():
    st.subheader("Profileinstellungen")
    
    user_data = get_user_data(st.session_state['username'])
    if user_data:
        age, weight, height = user_data
    else:
        age, weight, height = 0, 0, 0

    age = int(age) if age is not None else 0
    weight = int(weight) if weight is not None else 0
    height = int(height) if height is not None else 0
   
    age = st.number_input("Alter", min_value=0, max_value=120, step=1, value=age)
    weight = st.number_input("Gewicht", min_value=0, max_value=300, step=1, value=weight)
    height = st.number_input("Größe", min_value=0, max_value=300, step=1, value=height)

    if st.button("Speichern"):
        update_user(st.session_state['username'], age, weight, height)
        st.success("Profil aktualisiert!")
        st.experimental_rerun()
