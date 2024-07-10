import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import scipy.signal as signal
from test import run_streamlit_app  # Import der Funktion

class EKGdata:

    def __init__(self, df, person_info):
        self.df = df
        self.type = "Ruhe" if "Ruhe" in person_info.get('file_type', '') else "Belastung" if "Belastung" in person_info.get('file_type', '') else "Unbekannt"
        self.person_info = person_info
        self.df.columns = ['Time in s', 'ECG Signal (mV)']  # Rename columns for consistency
        self.ecg_signal = self.df['ECG Signal (mV)'].values
        self.time = self.df['Time in s'].values

    @staticmethod
    def find_peaks(series, threshold, distance):
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

        fig = px.line(filtered_df, x="Time in s", y='ECG Signal (mV)')
        fig.add_trace(go.Scatter(x=df["Time in s"].iloc[filtered_peaks], y=df["ECG Signal (mV)"].iloc[filtered_peaks], mode='markers', name='Peaks', marker=dict(color='red', size=8)))
        fig.update_layout(title='EKG über die Zeit', xaxis_title='Zeit in s', yaxis_title='EKG in mV')
        return fig
    
    @staticmethod
    def make_hf_plot(heart_rate_times, heart_rate_at_peaks, start_time, end_time):
        mask = (heart_rate_times >= start_time) & (heart_rate_times <= end_time)
        filtered_times = heart_rate_times[mask]
        filtered_hr = heart_rate_at_peaks[mask]

        df = pd.DataFrame({
            'Time in s': filtered_times,
            'Heart Rate (bpm)': filtered_hr
        })

        fig = px.line(df, x='Time in s', y='Heart Rate (bpm)')
        fig.update_layout(title='Herzfrequenz über die Zeit', xaxis_title='Zeit in s', yaxis_title='Herzfrequenz in bpm')
        return fig

    @staticmethod
    def plot_moving_average_heart_rate(heart_rate, heart_rate_time, window_size, start_time, end_time):
        mask = (heart_rate_time >= start_time) & (heart_rate_time <= end_time)
        filtered_heart_rate_time = heart_rate_time[mask]
        filtered_heart_rate = heart_rate[mask]

        if len(filtered_heart_rate) == 0:
            st.error("Nicht genügend Daten für die Berechnung des gleitenden Durchschnitts im ausgewählten Zeitbereich.")
            return go.Figure()

        smoothed_heart_rate = np.convolve(filtered_heart_rate, np.ones(window_size)/window_size, mode='valid')
        smoothed_heart_rate_time = filtered_heart_rate_time[:len(smoothed_heart_rate)]  # Zeitpunkte entsprechend anpassen

        df = pd.DataFrame({
            'Time in s': smoothed_heart_rate_time,
            'Smoothed Heart Rate (bpm)': smoothed_heart_rate
        })

        title = f"Geglättete Herzfrequenz über die Zeit (Gleitender Durchschnitt, Fenstergröße={window_size})"
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Time in s'], y=df['Smoothed Heart Rate (bpm)'], mode='lines+markers', name='Geglättete Herzfrequenz (bpm)'))
        fig.update_layout(
            title=title,
            xaxis_title='Zeit (s)',
            yaxis_title='Geglättete Herzfrequenz (bpm)',
            margin=dict(l=40, r=40, t=40, b=80),
        )
        
        explanation_text = (
            f"**Fenstergröße**: Die Anzahl der Datenpunkte, die im gleitenden Durchschnitt enthalten sind. "
            f"Eine Fenstergröße von {window_size} bedeutet, dass der Durchschnitt über {window_size} aufeinanderfolgende "
            f"Datenpunkte berechnet wird. Dies hilft, kurzfristige Schwankungen zu glätten und den zugrunde liegenden Trend deutlicher zu machen."
        )

        st.write(explanation_text)

        return fig

def display_hr_analysis():
    st.subheader("Herzfrequenzanalyse")
    if 'username' not in st.session_state:
        st.error("Sie müssen sich zuerst anmelden.")
        return

    username = st.session_state['username']
    st.text_input("Bestätigung des Benutzernamens", value=username, key="hr_username_input", disabled=True)

    if username in ["julian.huber", "yannic.heyer", "yunus.schmirander"]:
        run_streamlit_app(username)  # Aufruf der importierten Funktion mit dem Benutzernamen
    else:
        # Retrieve user profile from session state
        user_profile = st.session_state.get('user_profile', {})
        age = user_profile.get('age', 30)
        gender = user_profile.get('gender', 'unbekannt')

        st.write(f"Alter: {age} Jahre")
        st.write(f"Geschlecht: {gender}")

        person_info = {
            'name': username,
            'age': age,
            'gender': gender,
            'type': st.selectbox("Typ des EKGs", options=["Ruhe", "Belastung"], key="hr_type_selectbox")
        }
        uploaded_file = st.file_uploader("Laden Sie Ihre EKG-Daten hoch", type="csv", key="hr_file_uploader")
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.write("Hochgeladene Datei:")
            st.write(df.head())
            
            ekg_data = EKGdata(df, person_info)
            df = ekg_data.df
            peaks = EKGdata.find_peaks(df["ECG Signal (mV)"], 0.5, 200)
            heart_rate_times, heart_rate_at_peaks = EKGdata.estimate_hr(peaks, df["Time in s"])

            min_time = df["Time in s"].min()
            max_time = df["Time in s"].max()

            st.subheader("EKG und Herzfrequenzanalyse")

            st.write("Wählen Sie den Zeitbereich für den EKG-Plot aus:")
            start_time_ekg, end_time_ekg = st.slider(
                "Zeitbereich für EKG-Plot:",
                min_value=float(min_time),
                max_value=float(max_time),
                value=(float(min_time), float(max_time)),
                step=0.1,
                key="hr_ekg_slider"
            )

            ekg_fig = EKGdata.make_ekg_plot(peaks, df, start_time_ekg, end_time_ekg)
            st.plotly_chart(ekg_fig)

            st.subheader("Wählen Sie den Zeitbereich für den Herzfrequenz-Plot aus:")
            start_time_hr, end_time_hr = st.slider(
                "Zeitbereich für Herzfrequenz-Plot:",
                min_value=float(min_time),
                max_value=float(max_time),
                value=(float(min_time), float(max_time)),
                step=0.1,
                key="hr_hr_slider"
            )

            heart_rate_fig = EKGdata.make_hf_plot(heart_rate_times, heart_rate_at_peaks, start_time_hr, end_time_hr)
            st.plotly_chart(heart_rate_fig)

            st.subheader("Wählen Sie die Fenstergröße für den gleitenden Durchschnitt:")
            window_size = st.slider("Fenstergröße:", min_value=1, max_value=50, value=10, step=1, key="hr_window_slider")
            smoothed_heart_rate_fig = EKGdata.plot_moving_average_heart_rate(heart_rate_at_peaks, heart_rate_times, window_size, start_time_hr, end_time_hr)
            st.plotly_chart(smoothed_heart_rate_fig)

if __name__ == "__main__":
    display_hr_analysis()
