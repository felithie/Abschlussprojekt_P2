from user_data import load_user_data, save_user_data
from calculatemaxHR import calculate_hr 
import streamlit as st


def calculate_hrpage():
    users = load_user_data()
    user_info = users.get(st.session_state['username'], {})
    
    age = user_info.get('age')
    if age is None:
        age = st.number_input("Alter eingeben", min_value=1, max_value=120, step=1)
        if st.button("Alter speichern"):
            user_info['age'] = age
            users[st.session_state['username']] = user_info
            save_user_data(users)
            st.success("Alter gespeichert")
    else:
        st.write(f"Ihr Alter: {age}")
        max_hr = calculate_hr(age)
        st.write(f"Ihre maximale Herzfrequenz: {max_hr}")
    
    if st.button("Zurück zur Hauptseite"):
        st.session_state['page'] = 'main_page'