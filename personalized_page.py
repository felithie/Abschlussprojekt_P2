from calculatemaxHRpage import calculate_hrpage
from user_data import load_user_data, save_user_data
#import anmeldung1
import streamlit as st
import settings_page
def personalized_page():
    st.subheader(f"Willkommen, {st.session_state['username']}!")
    st.write("Wählen Sie eine Option:")
    
    if st.button("Maximale Herzfrequenz berechnen"):
        calculate_hrpage()

    if st.button("Abmelden"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = None
        st.session_state['page'] = 'main_page'
    
    if st.button("Benutzerdaten löschen"):
        users = load_user_data()
        users.pop(st.session_state['username'])
        save_user_data(users)
        st.session_state['logged_in'] = False
        st.session_state['username'] = None
        st.session_state['page'] = 'main_page'
    
    if st.button("Profieleinstellungen"):
        settings_page.user_profile_page()