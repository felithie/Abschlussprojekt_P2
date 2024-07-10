import os
import pandas as pd
import numpy as np
import scipy.signal as signal
from datetime import datetime
import streamlit as st
from versuch import display_in_streamlit  # Import der Funktion

class EKGdataHRV:
    def __init__(self, df, person_info):
        self.df = df
        self.type = "Ruhe" if "Ruhe" in person_info.get('type', '') else "Belastung" if "Belastung" in person_info.get('type', '') else "Unbekannt"
        self.df.columns = ['Time (s)', 'ECG Signal (mV)']  # Rename columns for consistency
        self.ecg_signal = self.df['ECG Signal (mV)'].values
        self.time = self.df['Time (s)'].values
        self.person_info = person_info
        self.r_peaks = self.find_r_peaks()  # Ensure r_peaks is always initialized

    @staticmethod
    def find_peaks(series, threshold, distance):
        if len(series) == 0:
            return np.array([]), {}
        peaks, properties = signal.find_peaks(series, height=threshold, distance=distance)
        return peaks, properties

    def find_r_peaks(self):
        r_peaks, _ = EKGdataHRV.find_peaks(self.ecg_signal, 0.5, 200)  # Adjust threshold and distance
        return r_peaks

    def find_nn_intervals(self):
        if len(self.time) == 0 or len(self.r_peaks) == 0:
            return np.array([])
        time = self.df['Time (s)'].values
        nn_intervals = np.diff(time[self.r_peaks])
        nn_intervals = nn_intervals[(nn_intervals > 0.3) & (nn_intervals < 2)]
        return nn_intervals

    @staticmethod
    def calculate_hrv(nn_intervals):
        if len(nn_intervals) == 0:
            return 0
        sdnn = np.std(nn_intervals, ddof=1)
        return sdnn

    def interpret_data(self):
        current_year = datetime.now().year
        age = self.person_info.get('age', 0)
        gender = self.person_info.get('gender', 'unbekannt')
        firstname = self.person_info.get('name', 'Unbekannt')

        interpretation = f"Diese HRV-Daten beziehen sich auf {firstname}, "
        interpretation += f"der/die {age} Jahre alt ist. "
        interpretation += f"Das Geschlecht der Person ist {gender}. "

        if self.type == "Belastung":
            interpretation += "Es handelt sich um ein Belastungs-EKG. Unter Belastung können HRV-Werte niedriger sein als im Ruhezustand. "
        else:
            interpretation += "Es handelt sich um ein Ruhe-EKG. "

        if age < 30:
            interpretation += "Für Personen unter 30 Jahren wird eine höhere HRV als gesund angesehen. "
        elif age < 50:
            interpretation += "Für Personen zwischen 30 und 50 Jahren wird eine moderate HRV als gesund angesehen. "
        else:
            interpretation += "Für Personen über 50 Jahren wird eine niedrigere HRV als gesund angesehen. "

        nn_intervals = self.find_nn_intervals()
        hrv = self.calculate_hrv(nn_intervals)
        interpretation += f"Die berechnete HRV (SDNN) beträgt {hrv:.2f} Sekunden. "

        if self.type == "Belastung":
            if hrv > 0.05:
                interpretation += "Dies deutet auf eine angemessene Herzfrequenzvariabilität unter Belastung hin."
            else:
                interpretation += "Eine HRV (SDNN) von unter 0.05 Sekunden unter Belastung kann auf eine geringe Herzfrequenzvariabilität hinweisen, was auf Stress oder mangelnde körperliche Anpassung hinweisen kann. Es wird empfohlen, dies weiter zu untersuchen."
        else:
            if hrv > 0.1:
                interpretation += "Dies deutet auf eine gute Herzfrequenzvariabilität hin."
            else:
                interpretation += "Eine HRV (SDNN) von unter 0.1 Sekunden kann auf eine geringe Herzfrequenzvariabilität hinweisen, was auf Stress, mangelnde körperliche Aktivität oder potenzielle Herzprobleme hinweisen kann. Es wird empfohlen, dies weiter zu untersuchen."

        return interpretation

def display_hrv_analysis():
    if 'username' not in st.session_state:
        st.error("Sie müssen sich zuerst anmelden.")
        return

    username = st.session_state['username']
    st.text_input("Bestätigung des Benutzernamens", value=username, key="username_input", disabled=True)

    if username in ["julian.huber", "yannic.heyer", "yunus.schmirander"]:
        display_in_streamlit(username)  # Aufruf der importierten Funktion mit dem Benutzernamen
    else:
        st.write("Geben Sie die Details für die HRV-Analyse ein")
        # Retrieve user profile from session state
        user_profile = st.session_state.get('user_profile', {})
        gender = user_profile.get('gender', 'unbekannt')

        person_info = {
            'name': username,
            'age': st.number_input("Alter", min_value=0, max_value=120, value=user_profile.get('age', 30)),
            'gender': gender,
            'type': st.selectbox("Typ des EKGs", options=["Ruhe", "Belastung"])
        }

        uploaded_file = st.file_uploader("Laden Sie Ihre EKG-Daten hoch", type="csv")
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.write("Hochgeladene Datei:")
            st.write(df.head())
            
            ekg_data = EKGdataHRV(df, person_info)
            nn_intervals = ekg_data.find_nn_intervals()
            hrv = EKGdataHRV.calculate_hrv(nn_intervals)

            st.write(f"**Herzfrequenzvariabilität (SDNN) in Sekunden:** {hrv:.4f} s")

            # Assuming the methods plot_poincare and plot_histogram exist
            poincare_fig = ekg_data.plot_poincare(nn_intervals)
            histogram_fig = ekg_data.plot_histogram(nn_intervals)
            interpretation = ekg_data.interpret_data()

            st.write("""
            ### Poincaré-Diagramm der NN-Intervalle
            """)
            st.plotly_chart(poincare_fig)

            st.write("""
            ### Histogramm der NN-Intervalle
            """)
            st.plotly_chart(histogram_fig)

            st.write("""
            ### Interpretation der HRV-Daten
            """)
            st.write(interpretation)

if __name__ == "__main__":
    display_hrv_analysis()
