import os
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

UPLOADS_DIR = "uploads"

def read_activity_csv(file):
    try:
        # Read the CSV file with the correct delimiter and header
        df = pd.read_csv(file, sep=",")
        
        # Verify the necessary columns exist
        if 'Duration' not in df.columns or 'PowerOriginal' not in df.columns:
            st.error("CSV file does not contain required columns: 'Duration' and 'PowerOriginal'")
            return None
        
        return df
    except Exception as e:
        st.error(f"Error reading the file: {e}")
        return None

def save_uploaded_file(uploaded_file, username):
    if not os.path.exists(UPLOADS_DIR):
        os.makedirs(UPLOADS_DIR)
    
    user_dir = os.path.join(UPLOADS_DIR, username)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    
    file_path = os.path.join(user_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path

def make_power_plot(df):
    fig = px.line(df, x="time", y="PowerOriginal")
    return fig

def find_best_effort(df, time, f_s):
    rolling_power = df["PowerOriginal"].rolling(window=int(time * f_s)).mean()
    max_power = rolling_power.max()
    return max_power  # Max power in the frame: time seconds, f_s Hz

def maxPowerValues(df):
    PowerValues = []
    intervals = [1, 30, 60, 300, 600, 1200]
    for interval in intervals:
        PowerValues.append(find_best_effort(df, interval, 1))
    PowerValuesD = {"Interval in s": intervals, "Power Values in W": PowerValues}
    df_pc = pd.DataFrame(PowerValuesD)
    return df_pc

def make_powerline_plot(df_pc):
    fig = px.line(df_pc, x="Interval in s", y="Power Values in W")
    fig.update_layout(title="Power Curve")
    return fig

def analyze_power_curve(df_pc):
    max_power_value = df_pc['Power Values in W'].max()
    min_power_value = df_pc['Power Values in W'].min()
    mean_power_value = df_pc['Power Values in W'].mean()
    std_power_value = df_pc['Power Values in W'].std()

    analysis = {
        "Maximale Leistung (W)": max_power_value,
        "Minimale Leistung (W)": min_power_value,
        "Durchschnittliche Leistung (W)": mean_power_value,
        "Standardabweichung der Leistung (W)": std_power_value,
    }

    return analysis

def display_power_curve():
    st.subheader("Leistungskurve")
    st.write("Laden Sie Ihre Aktivitätsdaten im CSV-Format hoch, um Ihre Leistungskurve zu analysieren.")

    uploaded_file = st.file_uploader("Upload your csv data file", type=["csv"])

    if uploaded_file is not None:
        username = st.session_state.get('username', 'guest')
        file_path = save_uploaded_file(uploaded_file, username)
        st.session_state['uploaded_file_path'] = file_path

    file_path = st.session_state.get('uploaded_file_path')
    if file_path:
        df = read_activity_csv(file_path)
        
        if df is not None:
           
            # Adding a time column if it doesn't exist
            if 'time' not in df.columns:
                df["time"] = np.arange(0, len(df))

            df_pc = maxPowerValues(df)
            fig = make_powerline_plot(df_pc)
            st.plotly_chart(fig)
            
            # Power Curve Analysis
            analysis = analyze_power_curve(df_pc)
            st.write("**Analyse:**")
            for key, value in analysis.items():
                st.write(f"{key}: {value:.2f}")
