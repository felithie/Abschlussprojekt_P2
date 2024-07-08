import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import scipy.signal as signal
from datetime import datetime

class EKGdata:

    # Konstruktor der Klasse soll die Daten einlesen
    def __init__(self, ekg_dict, person_info):
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.type = "Ruhe" if "Ruhe" in self.data else "Belastung" if "Belastung" in self.data else "Unbekannt"
        self.person_info = person_info
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
                    return ekg, person
        return None, None

    @staticmethod
    def find_peaks(series, threshold, distance):
        # Verwenden von scipy.signal.find_peaks zur Spitzenfindung
        peaks, _ = signal.find_peaks(series, height=threshold, distance=distance)
        return peaks

    @staticmethod
    def estimate_hr(peaks, time_in_s):
        peak_times_sec = time_in_s[peaks]
        rr_intervals = np.diff(peak_times_sec)
        heart_rate_at_peaks = 60 / rr_intervals
        heart_rate_times = peak_times_sec[1:]
        return heart_rate_times, heart_rate_at_peaks

    @staticmethod
    def make_ekg_plot(peaks, df, start_time, end_time):
        mask = (df["Time in s"] >= start_time) & (df["Time in s"] <= end_time)
        filtered_df = df[mask]
        filtered_peaks = [peak for peak in peaks if df["Time in s"].iloc[peak] >= start_time and df["Time in s"].iloc[peak] <= end_time]

        fig = px.line(filtered_df, x="Time in s", y='EKG in mV')
        fig.add_trace(go.Scatter(x=df["Time in s"].iloc[filtered_peaks], y=df["EKG in mV"].iloc[filtered_peaks], mode='markers', name='Peaks', marker=dict(color='red', size=8)))
        fig.update_layout(title='EKG über die Zeit', xaxis_title='Zeit in s', yaxis_title='EKG in mV')
        return fig
    
    @staticmethod
    def make_hf_plot(heart_rate_times, heart_rate_at_peaks, start_time, end_time):
        mask = (heart_rate_times >= start_time) & (heart_rate_times <= end_time)
        filtered_times = heart_rate_times[mask]
        filtered_hr = heart_rate_at_peaks[mask]

        fig = px.line(x=filtered_times, y=filtered_hr)
        fig.update_layout(title='Herzfrequenz über die Zeit', xaxis_title='Zeit in s', yaxis_title='Herzfrequenz in bpm')
        return fig

# Testen der Funktionen
if __name__ == "__main__":
    # Load the JSON data
    file = open("data/person_db.json")
    person_data = json.load(file)
    ekg_dict, person_info = EKGdata.load_by_id(1)
    
    if ekg_dict:
        # Create an instance of EKGdata
        ekg = EKGdata(ekg_dict, person_info)
        
        # Read EKG data from file
        df = pd.read_csv(ekg.data, sep='\t', header=None, names=['EKG in mV', 'Time in ms'])
        df["Time in s"] = df["Time in ms"] / 1000  # Convert milliseconds to seconds
        
        # Find peaks
        peaks = EKGdata.find_peaks(df["EKG in mV"].copy(), 340, 5)  # Adjust the threshold and distance values if necessary
        
        # Estimate heart rate
        heart_rate_times, heart_rate_at_peaks = EKGdata.estimate_hr(peaks, df["Time in s"])
        
        # Benutzerdefinierte Zeitbereiche festlegen
        min_time = df["Time in s"].min()
        max_time = df["Time in s"].max()

        st.header("EKG und Herzfrequenzanalyse")
        st.subheader(f"Patient: {person_info['firstname']} {person_info['lastname']} ({ekg.type} EKG)")

        st.subheader("Wählen Sie den Zeitbereich für den EKG-Plot aus:")
        start_time_ekg, end_time_ekg = st.slider(
            "Zeitbereich für EKG-Plot:",
            min_value=float(min_time),
            max_value=float(max_time),
            value=(float(min_time), float(max_time)),
            step=0.1
        )

        # EKG-Plot anzeigen
        ekg_fig = ekg.make_ekg_plot(peaks, df, start_time_ekg, end_time_ekg)
        st.plotly_chart(ekg_fig)

        st.subheader("Wählen Sie den Zeitbereich für den Herzfrequenz-Plot aus:")
        start_time_hr, end_time_hr = st.slider(
            "Zeitbereich für Herzfrequenz-Plot:",
            min_value=float(min_time),
            max_value=float(max_time),
            value=(float(min_time), float(max_time)),
            step=0.1
        )

        # Herzfrequenz-Plot anzeigen
        heart_rate_fig = ekg.make_hf_plot(heart_rate_times, heart_rate_at_peaks, start_time_hr, end_time_hr)
        st.plotly_chart(heart_rate_fig)
    else:
        st.error("Keine EKG-Daten gefunden.")
