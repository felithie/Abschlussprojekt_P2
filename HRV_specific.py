'''Diese ist ausschleißlich für julian.huber, yannic.heyer, yunus.schmirander '''
import json
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
import scipy.signal as signal
from datetime import datetime

class EKGdataHRV: # Klasse EKG-Data für Peakfinder, die uns ermöglicht peaks zu finden
    def __init__(self, ekg_dict, person_info):
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.type = "Ruhe" if "Ruhe" in self.data else "Belastung" if "Belastung" in self.data else "Unbekannt"
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['EKG in mV', 'Time in ms'])
        self.df["Time in s"] = self.df["Time in ms"] / 1000  # Convert milliseconds to seconds
        self.ecg_signal = self.df['EKG in mV'].values
        self.time = self.df['Time in s'].values
        self.person_info = person_info

    @staticmethod # um die Personendaten zu laden
    def load_person_data():
        with open("data/person_db.json") as file:
            return json.load(file)

    @staticmethod # um die Personendaten nach Benutzernamen zu laden
    def load_by_username(person_data, username):
        for person in person_data:
            if 'username' in person and person['username'] == username:
                return person
        return None

    @staticmethod #um die Peaks zu finden
    def find_peaks(series, threshold, distance):
        peaks, _ = signal.find_peaks(series, height=threshold, distance=distance)
        return peaks

    def find_r_peaks(self): #um die R-Peaks zu finden
        r_peaks = EKGdataHRV.find_peaks(self.ecg_signal, 340, 5)
        self.r_peaks = r_peaks
        return r_peaks

    def find_nn_intervals(self): #um die NN-Intervalle zu finden
        time = self.df['Time in s'].values
        nn_intervals = np.diff(time[self.find_r_peaks()])
        nn_intervals = nn_intervals[(nn_intervals > 0.3) & (nn_intervals < 2)]
        return nn_intervals

    @staticmethod #um die Herzfrequenzvariabilität zu berechnen
    def calculate_hrv(nn_intervals):
        if len(nn_intervals) > 0:
            sdnn = np.std(nn_intervals, ddof=1)
            return sdnn
        else:
            return 0

    def plot_poincare(self, nn_intervals):
        if len(nn_intervals) > 1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=nn_intervals[:-1], y=nn_intervals[1:], mode='markers', name='NN-Intervalle', marker=dict(color='blue', opacity=0.5)))
            fig.add_trace(go.Scatter(x=[min(nn_intervals), max(nn_intervals)], y=[min(nn_intervals), max(nn_intervals)], mode='lines', name='Identitätslinie', line=dict(color='red', dash='dash')))
            fig.update_layout(title='Poincaré-Diagramm der NN-Intervalle', xaxis_title='NN_i (s)', yaxis_title='NN_(i+1) (s)')
            return fig
        else:
            return go.Figure().update_layout(title='Poincaré-Diagramm der NN-Intervalle', xaxis_title='NN_i (s)', yaxis_title='NN_(i+1) (s)', annotations=[dict(text='Nicht genug Daten für das Diagramm', x=0.5, y=0.5, showarrow=False, font=dict(size=20))])
# Die Funktion plot_poincare erstellt ein Poincaré-Diagramm der NN-Intervalle. Das Poincaré-Diagramm ist eine grafische Darstellung der Herzfrequenzvariabilität (HRV), bei der die zeitlichen Abstände zwischen aufeinanderfolgenden Herzschlägen (NN-Intervalle) aufgetragen werden. Im Poincaré-Diagramm wird das NN-Intervall NN_i auf der x-Achse und das folgende Intervall NN_(i+1) auf der y-Achse dargestellt. Dies ermöglicht die Visualisierung der Dynamik und Variabilität der Herzfrequenz über die Zeit.
    
    def plot_histogram(self, nn_intervals):
        if len(nn_intervals) > 0:
            fig = go.Figure()
            fig.add_trace(go.Histogram(x=nn_intervals, nbinsx=50))
            fig.update_layout(title='Histogramm der NN-Intervalle', xaxis_title='NN-Intervall (s)', yaxis_title='Häufigkeit')
            return fig
        else:
            return go.Figure().update_layout(title='Histogramm der NN-Intervalle', xaxis_title='NN-Intervall (s)', yaxis_title='Häufigkeit', annotations=[dict(text='Nicht genug Daten für das Histogramm', x=0.5, y=0.5, showarrow=False, font=dict(size=20))])
# Die Funktion plot_histogram erstellt ein Histogramm der NN-Intervalle. Ein Histogramm ist eine grafische Darstellung der Verteilung eines Datensatzes. In Bezug auf die HRV zeigt ein Histogramm die Häufigkeit der verschiedenen NN-Intervalle (zeitliche Abstände zwischen Herzschlägen) in einem bestimmten Zeitraum.

    def interpret_data(self):
        current_year = datetime.now().year
        birth_year = self.person_info.get('date_of_birth', 1980)
        age = current_year - birth_year
        gender = self.person_info.get('gender', 'unbekannt')
        firstname = self.person_info.get('firstname', 'Unbekannt')
        lastname = self.person_info.get('lastname', 'Unbekannt')

        interpretation = f"Diese HRV-Daten beziehen sich auf {firstname} {lastname}, "
        interpretation += f"der/die im Jahr {birth_year} geboren wurde und somit {age} Jahre alt ist. "
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
'''Die Funktion interpret_data erstellt eine Interpretation der HRV-Daten basierend auf den berechneten Werten und den Personendaten. Die Interpretation enthält Informationen über die Person (Name, Alter, Geschlecht), den Typ des EKGs (Ruhe oder Belastung), die HRV-Werte und eine Bewertung der HRV basierend auf dem Alter und Geschlecht der Person. Die Interpretation gibt auch Empfehlungen für den Fall, dass die HRV-Werte außerhalb des normalen Bereichs liegen.'''

def display_in_streamlit(username):
    person_data = EKGdataHRV.load_person_data()
    selected_person = EKGdataHRV.load_by_username(person_data, username)

    if selected_person:
        # Extract gender from session state if available
        user_profile = st.session_state.get('user_profile', {})
        gender = user_profile.get('gender', 'unbekannt')
        selected_person['gender'] = gender

        ekg_options = {f"EKG ID {ekg['id']} - {ekg['date']}": ekg for ekg in selected_person['ekg_tests']}
        selected_ekg = st.selectbox("Wählen Sie ein EKG aus:", list(ekg_options.keys()), key="ekg_select")
        selected_ekg_data = ekg_options[selected_ekg]

        ekg_data = EKGdataHRV(selected_ekg_data, selected_person)
        nn_intervals = ekg_data.find_nn_intervals()
        hrv = EKGdataHRV.calculate_hrv(nn_intervals)

        st.write(f"**Herzfrequenzvariabilität (SDNN) in Sekunden:** {hrv:.4f} s")

        poincare_fig = ekg_data.plot_poincare(nn_intervals)
        histogram_fig = ekg_data.plot_histogram(nn_intervals)
        interpretation = ekg_data.interpret_data()

        st.plotly_chart(poincare_fig)
        st.write("""
        Das **Poincaré-Diagramm** ist eine grafische Darstellung der Herzfrequenzvariabilität (HRV), bei der die zeitlichen Abstände zwischen aufeinanderfolgenden Herzschlägen (NN-Intervalle) aufgetragen werden. Im Poincaré-Diagramm wird das NN-Intervall \(NN_i\) auf der x-Achse und das folgende Intervall \(NN_{i+1}\) auf der y-Achse dargestellt. Dies ermöglicht die Visualisierung der Dynamik und Variabilität der Herzfrequenz über die Zeit.

        - **Form und Verteilung**: Die Form und Verteilung der Punkte im Diagramm geben Aufschluss über die HRV. Eine dichte Punktwolke um die Identitätslinie (diagonale Linie) deutet auf eine geringe Variabilität hin, während eine breitere Streuung auf eine höhere Variabilität hinweist.
        - **Anwendungsgebiete**: Poincaré-Diagramme werden in der kardiologischen Forschung und in klinischen Anwendungen verwendet, um Herzrhythmusstörungen zu erkennen und die allgemeine Gesundheit des Herz-Kreislauf-Systems zu beurteilen.
        """)

        st.plotly_chart(histogram_fig)
        st.write("""
        Ein **Histogramm** ist eine grafische Darstellung der Verteilung eines Datensatzes. In Bezug auf die HRV zeigt ein Histogramm die Häufigkeit der verschiedenen NN-Intervalle (zeitliche Abstände zwischen Herzschlägen) in einem bestimmten Zeitraum.

        - **Achsen**: Auf der x-Achse werden die NN-Intervalle aufgetragen, und auf der y-Achse wird die Häufigkeit dieser Intervalle angezeigt.
        - **Interpretation**: Ein Histogramm kann helfen, die Verteilung und Häufigkeit bestimmter NN-Intervalle zu verstehen. Ein breites Histogramm mit einer flachen Verteilung deutet auf eine hohe Variabilität der Herzfrequenz hin, während ein schmales Histogramm mit einem ausgeprägten Peak auf eine geringe Variabilität hinweist.
        - **Anwendungsgebiete**: Histogramme werden verwendet, um die allgemeine Variabilität der Herzfrequenz zu beurteilen und Anomalien oder Muster in der HRV zu identifizieren.
        """)


        st.write("""
        ### Interpretation der HRV-Daten
        """)
        st.write(interpretation)
    else:
        st.write("Benutzername nicht gefunden. Bitte überprüfen Sie Ihre Eingabe.")
'''Die Funktion display_in_streamlit ermöglicht es uns, die HRV-Daten in Streamlit anzuzeigen. Sie lädt die Personendaten und das ausgewählte EKG basierend auf dem Benutzernamen und zeigt die berechnete Herzfrequenzvariabilität (HRV) sowie die Poincaré-Diagramme und Histogramme der NN-Intervalle an. Die Funktion erstellt auch eine Interpretation der HRV-Daten basierend auf den berechneten Werten und den Personendaten. Die Interpretation enthält Informationen über die Person (Name, Alter, Geschlecht), den Typ des EKGs (Ruhe oder Belastung), die HRV-Werte und eine Bewertung der HRV basierend auf dem Alter und Geschlecht der Person. Die Interpretation gibt auch Empfehlungen für den Fall, dass die HRV-Werte außerhalb des normalen Bereichs liegen.'''