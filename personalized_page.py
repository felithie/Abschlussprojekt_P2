#personalized_page.py
import streamlit as st
from calculatemaxHRpage import calculate_hrpage
from settings_page import user_profile_page
from CalculateBMI import calculateBMI_page
def personalized_page():
    st.subheader(f"Willkommen, {st.session_state['username']}!")
    st.write("Wählen Sie eine Option:")

    tabs = st.tabs(["Herzfrequenz berechnen", "Abmelden", "Profileinstellungen", "BMI berechnen"])

    with tabs[0]:
        if st.button("Maximale Herzfrequenz berechnen"):
            calculate_hrpage()

    with tabs[1]:
        if st.button("Abmelden"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = None
            st.session_state['page'] = 'main_page'
            st.experimental_rerun()

    with tabs[2]:
        user_profile_page()

    with tabs[3]:
        calculateBMI_page()

        
