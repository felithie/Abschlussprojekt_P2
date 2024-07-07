import json
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
import scipy.signal as signal

class EKGdataHRV:

    # Konstruktor der Klasse soll die Daten einlesen
    def __init__(self, ekg_dict):
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['EKG in mV', 'Time in ms'])
        self.df["Time in s"] = self.df["Time in ms"] / 1000  # Convert milliseconds to seconds
        self.ecg_signal = self.df['EKG in mV'].values
        self.time = self.df['Time in s'].values

    @staticmethod
    def load_by_id(ekg_id):
        with open("data/person_db.json") as file:
            person_data = json.load(file)
        for person in person_data:
            ekg_tests = person['ekg_tests']
            for ekg in ekg_tests:
                if ekg["id"] == ekg_id:
                    return ekg
        return None

    @staticmethod
    def find_peaks(series, threshold, distance):
        # Verwenden von scipy.signal.find_peaks, um die Spitzen im EKG-Signal zu finden
        peaks, _ = signal.find_peaks(series, height=threshold, distance=distance)
        return peaks
    
    def find_r_peaks(self):
        r_peaks = EKGdataHRV.find_peaks(self.ecg_signal, 340, 0.6 * 1000)
        self.r_peaks = r_peaks
        return r_peaks
    
    def find_nn_intervals(self):
        """
        Berechnet die NN-Intervalle basierend auf den gefundenen R-Zacken.

        Rückgabe:
        list of float: Liste der NN-Intervalle (in Sekunden).
        """
        time = self.df['Time in s'].values 
        nn_intervals = np.diff(time[self.find_r_peaks()])
        return nn_intervals
    
    @staticmethod
    def calculate_hrv(nn_intervals):
        """
        Berechnet die Herzfrequenzvariabilität (HRV) basierend auf den NN-Intervallen.

        Parameter:
        nn_intervals (list of float): Liste der NN-Intervalle (in Sekunden).

        Rückgabe:
        float: HRV-Wert (SDNN in Sekunden).
        """
        # Berechnung der Standardabweichung der NN-Intervalle (SDNN)
        sdnn = np.std(nn_intervals, ddof=1)
        return sdnn
    
    def plot_poincare(self, nn_intervals):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=nn_intervals[:-1], y=nn_intervals[1:], mode='markers', name='NN-Intervalle', marker=dict(color='blue', opacity=0.5)))
        fig.add_trace(go.Scatter(x=[min(nn_intervals), max(nn_intervals)], y=[min(nn_intervals), max(nn_intervals)], mode='lines', name='Identitätslinie', line=dict(color='red', dash='dash')))
        fig.update_layout(title='Poincaré-Diagramm der NN-Intervalle', xaxis_title='NN_i (s)', yaxis_title='NN_(i+1) (s)')
        return fig
    
    def plot_histogram(self, nn_intervals):
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=nn_intervals, nbinsx=50))
        fig.update_layout(title='Histogramm der NN-Intervalle', xaxis_title='NN-Intervall (s)', yaxis_title='Häufigkeit')
        return fig

if __name__ == "__main__":
    ekg_dict = EKGdataHRV.load_by_id(1)
    ekg_data = EKGdataHRV(ekg_dict)

    nn_intervals = ekg_data.find_nn_intervals()
    hrv = EKGdataHRV.calculate_hrv(nn_intervals)
    print(f"Herzfrequenzvariabilität (SDNN) in Sekunden: {hrv:.4f} s")
    poincare_fig = ekg_data.plot_poincare(nn_intervals)
    histogram_fig = ekg_data.plot_histogram(nn_intervals)

    st.title("HRV-Analyse")
    st.write(f"**Herzfrequenzvariabilität (SDNN) in Sekunden:** `{hrv:.4f} s`")
    st.plotly_chart(poincare_fig)
    st.plotly_chart(histogram_fig)