import streamlit as st
from calculatemaxHRpage import calculate_hrpage
from settings_page import user_profile_page

def personalized_page():
    st.subheader(f"Willkommen, {st.session_state['username']}!")
    st.write("Wählen Sie eine Option:")

    tabs = st.tabs(["Herzfrequenz berechnen", "Abmelden", "Profieleinstellungen"])
    
    with tabs[0]:    
       if st.button("Maximale Herzfrequenz berechnen"):
        calculate_hrpage()
    
    with tabs[1]:
        if st.button("Abmelden"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = None
            st.session_state['page'] = 'main_page'
            st.experimental_rerun()
        # Uncomment these lines if you want to add user data deletion functionality
        # if st.button("Benutzerdaten löschen"):
        #    users = load_user_data()
        #    users.pop(st.session_state['username'], None)
        #    save_user_data(users)
        #    st.session_state['logged_in'] = False
        #    st.session_state['username'] = None
        #    st.session_state['page'] = 'main_page'
        #    st.experimental_rerun()
    
    with tabs[2]:   
        #if st.button("Profieleinstellungen"):
        user_profile_page()