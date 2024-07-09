import streamlit as st
from calculatemaxHRpage import calculate_hrpage
from settings_page import user_profile_page
from CalculateBMI import calculate_bmi_page
from HRV import display_hrv_analysis
from HR import display_hr_analysis
from Powercurve import display_power_curve

def personalized_page():
    st.subheader(f"Willkommen, {st.session_state['username']}!")
    st.write("Wählen Sie eine Option:")

    tabs = st.tabs(["Herzfrequenz berechnen", "Abmelden", "Profileinstellungen", "BMI berechnen", "HRV Analyse", "HR Analyse", "Leistungskurve"])

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
        calculate_bmi_page()
    
    with tabs[4]:
        display_hrv_analysis()
        
    with tabs[5]:
        display_hr_analysis()

    with tabs[6]:
        display_power_curve()
