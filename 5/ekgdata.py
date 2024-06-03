import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# %% Objekt-Welt

# Klasse EKG-Data für Peakfinder, die uns ermöglicht peaks zu finden

class EKGdata:

    # Konstruktor der Klasse soll die Daten einlesen
    def __init__(self, ekg_dict):
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['EKG in mV', 'Time in ms'])
        self.df["Time in s"] = self.df["Time in ms"] / 1000  # Convert milliseconds to seconds

    @staticmethod
    def load_by_id(ekg_id):
        file = open("data/person_db.json")
        person_data = json.load(file)
        for person in person_data:
            ekg_tests = person['ekg_tests']
            for ekg in ekg_tests:
                if ekg["id"] == ekg_id:
                    return ekg
        return None

    @staticmethod
    def find_peaks(series, threshold, respacing_factor=5):
        # Respace the series
        series = series.iloc[::respacing_factor]
        # Filter the series
        series = series[series > threshold]

        peaks = []
        last = 0
        current = 0
        next = 0

        for index, row in series.items():
            last = current
            current = next
            next = row

            if last < current and current > next and current > threshold:
                peaks.append(index - respacing_factor)

        return peaks

    @staticmethod
    def estimate_hr(peaks):
        peak_times_sec = np.array(peaks) / 1000
        rr_intervals = np.diff(peak_times_sec)
        heart_rate_at_peaks = 60 / rr_intervals
        heart_rate_times = peak_times_sec[1:]
        return heart_rate_times, heart_rate_at_peaks

    @staticmethod
    def make_ekg_plot(peaks, df):
        fig = px.line(df, x="Time in s", y='EKG in mV')
        fig.add_trace(go.Scatter(x=df["Time in s"].iloc[peaks], y=df["EKG in mV"].iloc[peaks], mode='markers', name='Peaks', marker=dict(color='red', size=8)))
        fig.update_layout(title='EKG over Time', xaxis_title='Time in s', yaxis_title='EKG in mV')
        return fig
    
    @staticmethod
    def make_hf_plot(heart_rate_times, heart_rate_at_peaks):
        fig = px.line(x=heart_rate_times, y=heart_rate_at_peaks)
        fig.update_layout(title='Heart Rate over Time', xaxis_title='Time in s', yaxis_title='Heart Rate in bpm')
        return fig

# %% Testen der Funktionen

if __name__ == "__main__":
    # Load the JSON data
    file = open("data/person_db.json")
    person_data = json.load(file)
    ekg_dict = person_data[0]["ekg_tests"][0]
    
    # Create an instance of EKGdata
    ekg = EKGdata(ekg_dict)
    
    # Load EKG data by ID
    Ekg_1 = EKGdata.load_by_id(1)
    
    # Read EKG data from file
    df = pd.read_csv(r'data/ekg_data/01_Ruhe.txt', sep='\t', header=None, names=['EKG in mV', 'Time in ms'])
    df["Time in s"] = df["Time in ms"] / 1000  # Convert milliseconds to seconds
    
    # Find peaks
    peaks = EKGdata.find_peaks(df["EKG in mV"].copy(), 340, 5)
    
    # Estimate heart rate
    heart_rate_times, heart_rate_at_peaks = EKGdata.estimate_hr(peaks)
    
    # Create and display the EKG plot
    fig = EKGdata.make_ekg_plot(peaks, df)
    fig.show()

    # Create and display the heart rate plot

    fig = EKGdata.make_hf_plot(heart_rate_times, heart_rate_at_peaks)
    fig.show()