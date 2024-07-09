import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

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

# Streamlit interface
st.title("EKG Power Curve Visualization")

uploaded_file = st.file_uploader("Upload your EKG data file", type=["csv", "txt"])

if uploaded_file is not None:
    df = read_activity_csv(uploaded_file)
    
    if df is not None:
        st.write("Data Preview:")
        st.write(df.head())
        
        # Adding a time column if it doesn't exist
        if 'time' not in df.columns:
            df["time"] = np.arange(0, len(df))

        df_pc = maxPowerValues(df)
        fig = make_powerline_plot(df_pc)
        st.plotly_chart(fig)