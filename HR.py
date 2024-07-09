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

    @staticmethod
    def plot_moving_average_heart_rate(heart_rate, heart_rate_time, window_size, start_time, end_time):
        """
        Erstellt ein Plot der geglätteten Herzfrequenz über die Zeit.

        Parameter:
        heart_rate (list of float): Liste der Herzfrequenzen (in bpm).
        heart_rate_time (list of float): Liste der Zeitpunkte (in s) für die Herzfrequenzen.
        window_size (int): Die Fenstergröße für den gleitenden Durchschnitt.
        start_time (float): Startzeitpunkt für den Plot (in s).
        end_time (float): Endzeitpunkt für den Plot (in s).

        Rückgabe:
        plotly.graph_objects.Figure: Plotly-Figur.
        """
        # Filtere die Daten nach dem ausgewählten Zeitbereich
        mask = (heart_rate_time >= start_time) & (heart_rate_time <= end_time)
        filtered_heart_rate_time = heart_rate_time[mask]
        filtered_heart_rate = heart_rate[mask]

        smoothed_heart_rate = np.convolve(filtered_heart_rate, np.ones(window_size)/window_size, mode='valid')
        smoothed_heart_rate_time = filtered_heart_rate_time[:len(smoothed_heart_rate)]  # Zeitpunkte entsprechend anpassen

        title = f"Geglättete Herzfrequenz über die Zeit (Gleitender Durchschnitt, Fenstergröße={window_size})"
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=smoothed_heart_rate_time, y=smoothed_heart_rate, mode='lines+markers', name='Geglättete Herzfrequenz (bpm)'))
        fig.update_layout(
            title=title,
            xaxis_title='Zeit (s)',
            yaxis_title='Geglättete Herzfrequenz (bpm)',
            margin=dict(l=40, r=40, t=40, b=80),
        )
        
        # Erklärung zur Fenstergröße als separater Text
        explanation_text = (
            f"**Fenstergröße**: Die Anzahl der Datenpunkte, die im gleitenden Durchschnitt enthalten sind. "
            f"Eine Fenstergröße von {window_size} bedeutet, dass der Durchschnitt über {window_size} aufeinanderfolgende "
            f"Datenpunkte berechnet wird. Dies hilft, kurzfristige Schwankungen zu glätten und den zugrunde liegenden Trend deutlicher zu machen."
        )

        # Anzeige der Erklärung in Streamlit
        st.write(explanation_text)

        return fig

# Testen der Funktionen
if __name__ == "__main__":
    # Load the JSON data
    file = open("data/person_db.json")
    person_data = json.load(file)
    ekg_dict, person_info = EKGdata.load_by_id(4)
    
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

         # Gleitender Durchschnitt der Herzfrequenz anzeigen
        st.subheader("Wählen Sie die Fenstergröße für den gleitenden Durchschnitt:")
        window_size = st.slider("Fenstergröße:", min_value=1, max_value=50, value=10, step=1)
        smoothed_heart_rate_fig = EKGdata.plot_moving_average_heart_rate(heart_rate_at_peaks, heart_rate_times, window_size, start_time_hr, end_time_hr)
        st.plotly_chart(smoothed_heart_rate_fig)

    else:
        st.error("Keine EKG-Daten gefunden.")
