import streamlit as st
from calculatemaxHRpage import calculate_hrpage
from settings_page import user_profile_page
from CalculateBMI import calculate_bmi_page
from EKGdataHRV_Plots import display_hrv_analysis
from HR import display_hr_analysis
from Powercurve import display_power_curve

def personalized_page():
    st.subheader(f"Willkommen, {st.session_state['username']}!")
    st.write("Wählen Sie eine Option:")

    tabs = st.tabs(["Profileinstellungen", "HR Analyse", "HRV Analyse",  "BMI berechnen", "Maximale Herzfrequenz berechnen", "Leistungskurve", "Abmelden"])

    with tabs[0]:
        user_profile_page()

    with tabs[1]:
        display_hr_analysis()

    with tabs[2]:
        display_hrv_analysis()
        
    with tabs[3]:
        calculate_bmi_page()
    
    with tabs[4]:
        calculate_hrpage()
        
    with tabs[5]:
        display_power_curve()

    with tabs[6]:
        if st.button("Abmelden"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = None
            st.session_state['page'] = 'main_page'
            st.experimental_rerun()