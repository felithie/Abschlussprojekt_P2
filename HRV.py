import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import scipy.signal as signal
from datetime import datetime
import streamlit as st
from database import get_user_id, get_user_files, get_user_data

class EKGdataHRV:

    def __init__(self, file_path, person_info):
        self.file_path = file_path
        self.type = "Ruhe" if "Ruhe" in self.file_path else "Belastung" if "Belastung" in self.file_path else "Unbekannt"
        self.df = pd.read_csv(self.file_path)
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
        r_peaks, _ = EKGdataHRV.find_peaks(self.ecg_signal, 340, 5)
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

    def plot_poincare(self, nn_intervals):
        if len(nn_intervals) > 1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=nn_intervals[:-1], y=nn_intervals[1:], mode='markers', name='NN-Intervalle', marker=dict(color='blue', opacity=0.5)))
            fig.add_trace(go.Scatter(x=[min(nn_intervals), max(nn_intervals)], y=[min(nn_intervals), max(nn_intervals)], mode='lines', name='Identitätslinie', line=dict(color='red', dash='dash')))
            fig.update_layout(title='Poincaré-Diagramm der NN-Intervalle', xaxis_title='NN_i (s)', yaxis_title='NN_(i+1) (s)')
            return fig
        else:
            return go.Figure().update_layout(title='Poincaré-Diagramm der NN-Intervalle', xaxis_title='NN_i (s)', yaxis_title='NN_(i+1) (s)', annotations=[dict(text='Nicht genug Daten für das Diagramm', x=0.5, y=0.5, showarrow=False, font=dict(size=20))])

    def plot_histogram(self, nn_intervals):
        if len(nn_intervals) > 0:
            fig = go.Figure()
            fig.add_trace(go.Histogram(x=nn_intervals, nbinsx=min(50, len(nn_intervals))))
            fig.update_layout(title='Histogramm der NN-Intervalle', xaxis_title='NN-Intervall (s)', yaxis_title='Häufigkeit')
            return fig
        else:
            return go.Figure().update_layout(title='Histogramm der NN-Intervalle', xaxis_title='NN-Intervall (s)', yaxis_title='Häufigkeit', annotations=[dict(text='Nicht genug Daten für das Histogramm', x=0.5, y=0.5, showarrow=False, font=dict(size=20))])

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
    username = st.session_state.get('username')
    if not username:
        st.error("Bitte melden Sie sich an.")
        return

    user_id = get_user_id(username)
    if not user_id:
        st.error("Benutzer nicht gefunden.")
        return

    files = get_user_files(user_id)
    if not files:
        st.error("Keine EKG-Daten gefunden.")
        return

    selected_file = st.selectbox("Wählen Sie eine Datei zur Analyse", files, key="ekg_selectbox")
    if selected_file:
        person_info = get_user_data(username)
        if person_info:
            person_info = {
                'age': person_info[0],
                'weight': person_info[1],
                'height': person_info[2],
                'name': username,  # Using username as the name since the actual name field is not retrieved
                'gender': person_info[7]  # Retrieve gender from the database
            }
        ekg_data = EKGdataHRV(selected_file, person_info)
        nn_intervals = ekg_data.find_nn_intervals()
        hrv = EKGdataHRV.calculate_hrv(nn_intervals)

        st.write(f"**Herzfrequenzvariabilität (SDNN) in Sekunden:** `{hrv:.4f} s`")

        poincare_fig = ekg_data.plot_poincare(nn_intervals)
        histogram_fig = ekg_data.plot_histogram(nn_intervals)
        interpretation = ekg_data.interpret_data()

        st.plotly_chart(poincare_fig)
        st.plotly_chart(histogram_fig)
        st.write(interpretation)

if __name__ == "__main__":
    display_hrv_analysis()
