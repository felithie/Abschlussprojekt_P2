from calculatemaxHRpage import calculate_hrpage
from user_data import load_user_data, save_user_data
import anmeldung1
import streamlit as st

def personalized_page():
    st.subheader(f"Willkommen, {st.session_state['username']}!")
    st.write("Wählen Sie eine Option:")
    
    if st.button("Maximale Herzfrequenz berechnen"):
        calculate_hrpage()
