import json
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
import scipy.signal as signal

class EKGdataHeartRate:

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
        """
        Findet die R-Zacken im EKG-Signal.

        Parameter:
        series (numpy.ndarray): EKG-Signal.
        threshold (float): Schwellenwert zur Erkennung der R-Zacken.
        distance (float): Mindestabstand zwischen den R-Zacken.

        Rückgabe:
        numpy.ndarray: Indizes der erkannten R-Zacken.
        """
        peaks, _ = signal.find_peaks(series, height=threshold, distance=distance)
        return peaks
    
    def find_r_peaks(self):
        """
        Findet und speichert die R-Zacken im EKG-Signal.

        Rückgabe:
        numpy.ndarray: Indizes der erkannten R-Zacken.
        """
        r_peaks = EKGdataHeartRate.find_peaks(self.ecg_signal, 340, 0.6 * 1000)
        self.r_peaks = r_peaks
        return r_peaks
    
    def calculate_heart_rate_from_rr(self):
        """
        Berechnet die Herzfrequenz (in bpm) basierend auf den RR-Intervallen.
        Die Zeitpunkte der Herzfrequenz entsprechen den Zeitpunkten der ersten R-Zacke jedes Intervalls.

        Rückgabe:
        tuple: (Liste der Herzfrequenzen (in bpm), Liste der Zeitpunkte (in s) für die Herzfrequenzen).
        """
        rr_intervals = np.diff(self.time[self.r_peaks])
        heart_rate = 60 / rr_intervals  # Umwandlung von Sekunden in bpm
        return heart_rate, self.time[self.r_peaks[:-1]]

    def calculate_moving_average(self, data, window_size):
        """
        Berechnet den gleitenden Durchschnitt einer Datenreihe.

        Parameter:
        data (list of float): Die Datenreihe.
        window_size (int): Die Fenstergröße für den gleitenden Durchschnitt.

        Rückgabe:
        numpy.ndarray: Die geglätteten Daten.
        """
        return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

    def plot_heart_rate(self, heart_rate, heart_rate_time, start_time, end_time):
        """
        Erstellt ein Plot der Herzfrequenz über die Zeit.

        Parameter:
        heart_rate (list of float): Liste der Herzfrequenzen (in bpm).
        heart_rate_time (list of float): Liste der Zeitpunkte (in s) für die Herzfrequenzen.
        start_time (float): Startzeitpunkt für den Plot (in s).
        end_time (float): Endzeitpunkt für den Plot (in s).

        Rückgabe:
        plotly.graph_objects.Figure: Plotly-Figur.
        """
        title = "Herzfrequenz über die Zeit (RR-Intervalle)"
        
        # Filtere die Daten nach dem ausgewählten Zeitbereich
        mask = (heart_rate_time >= start_time) & (heart_rate_time <= end_time)
        filtered_heart_rate_time = heart_rate_time[mask]
        filtered_heart_rate = heart_rate[mask]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=filtered_heart_rate_time, y=filtered_heart_rate, mode='lines+markers', name='Herzfrequenz (bpm)'))
        fig.update_layout(title=title, xaxis_title='Zeit (s)', yaxis_title='Herzfrequenz (bpm)')
        return fig

    def plot_moving_average_heart_rate(self, heart_rate, heart_rate_time, window_size, start_time, end_time):
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

        smoothed_heart_rate = self.calculate_moving_average(filtered_heart_rate, window_size)
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


    def plot_ekg(self, start_time, end_time):
        """
        Erstellt ein Plot des EKG-Signals und markiert die R-Zacken.

        Rückgabe:
        plotly.graph_objects.Figure: Plotly-Figur.
        """
        r_peaks = self.find_peaks(self.ecg_signal, 340, 0.6 * 1000)

        # Filtere die Daten nach dem ausgewählten Zeitbereich
        mask = (self.time >= start_time) & (self.time <= end_time)
        filtered_time = self.time[mask]
        filtered_ecg_signal = self.ecg_signal[mask]

        # Filtere die R-Peaks nach dem ausgewählten Zeitbereich
        filtered_r_peaks = [peak for peak in r_peaks if self.time[peak] >= start_time and self.time[peak] <= end_time]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=filtered_time, y=filtered_ecg_signal, mode='lines', name='EKG-Signal'))
        fig.add_trace(go.Scatter(x=self.time[filtered_r_peaks], y=self.ecg_signal[filtered_r_peaks], mode='markers', name='R-Zacken', marker=dict(color='red')))
        fig.update_layout(title='EKG-Signal mit identifizierten R-Zacken', xaxis_title='Zeit (s)', yaxis_title='Messwerte (mV)')
        return fig
        
if __name__ == "__main__":
    ekg_dict = EKGdataHeartRate.load_by_id(1)
    ekg_data = EKGdataHeartRate(ekg_dict)

    # Herzfrequenz basierend auf den RR-Intervallen
    ekg_data.find_r_peaks()
    heart_rate_rr, heart_rate_rr_time = ekg_data.calculate_heart_rate_from_rr()

    # Benutzerdefinierte Zeitbereiche festlegen
    min_time = ekg_data.time.min()
    max_time = ekg_data.time.max()

    st.header("EKG und Herzfrequenzanalyse")

    st.subheader("Wählen Sie den Zeitbereich für den EKG-Plot aus:")
    start_time_ekg, end_time_ekg = st.slider(
        "Zeitbereich für EKG-Plot:",
        min_value=float(min_time),
        max_value=float(max_time),
        value=(float(min_time), float(max_time)),
        step=0.1
    )

    # EKG-Plot anzeigen
    ekg_fig = ekg_data.plot_ekg(start_time_ekg, end_time_ekg)
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
    heart_rate_rr_fig = ekg_data.plot_heart_rate(heart_rate_rr, heart_rate_rr_time, start_time_hr, end_time_hr)
    st.plotly_chart(heart_rate_rr_fig)

    # Gleitender Durchschnitt der Herzfrequenz anzeigen
    st.subheader("Wählen Sie die Fenstergröße für den gleitenden Durchschnitt:")
    window_size = st.slider("Fenstergröße:", min_value=1, max_value=50, value=10, step=1)
    smoothed_heart_rate_fig = ekg_data.plot_moving_average_heart_rate(heart_rate_rr, heart_rate_rr_time, window_size, start_time_hr, end_time_hr)
    st.plotly_chart(smoothed_heart_rate_fig)
