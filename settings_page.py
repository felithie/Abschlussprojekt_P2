from user_data import load_user_data, save_user_data
import streamlit as st

def user_profile_page():
    users = load_user_data()
    user_info = users.get(st.session_state['username'], {})
    
    # Benutzerdaten für den aktuellen Benutzer abrufen
    age = user_info.get('age')
    weight = user_info.get('weight')
    height = user_info.get('height')
    password = user_info.get('password')

    #Benutzerdaten bearbeiten
    st.subheader("Benutzerdaten bearbeiten")
    age = st.number_input("Alter", min_value=0, max_value=150, value=age)
    weight = st.number_input("Gewicht (kg)", min_value=0, value=weight)
    height = st.number_input("Größe (cm)", min_value=0, value=height)
    password = st.text_input("Passwort", type="password", value=password)
    
    # Benutzerdaten aktualisieren
    user_info['age'] = age
    user_info['weight'] = weight
    user_info['height'] = height
    user_info['password'] = password
    users[st.session_state['username']] = user_info
    save_user_data(users)
    
    
    
    
    if st.button("Zurück zur Hauptseite"):
        st.session_state['page'] = 'main_page'
        st.experimental_rerun()
