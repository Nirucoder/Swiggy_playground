import pandas as pd
import streamlit as st
import json
import os
from src.config.settings import FINAL_TRAINING_DATA, HOURLY_TRAINING_DATA, FORECAST_SUMMARY

@st.cache_data
def load_historical_data():
    """Loads and preprocesses historical training data."""
    df = pd.read_csv(FINAL_TRAINING_DATA)
    df['ds'] = pd.to_datetime(df['ds'])
    
    # Add display names by removing prefixes
    prefixes = ['Indian ', 'Italian ', 'Thai ', 'Continental ']
    df['display_name'] = df['category']
    for p in prefixes:
        df['display_name'] = df['display_name'].str.replace(p, '')
        
    return df

@st.cache_data
def load_hourly_data():
    """Loads hourly training data."""
    return pd.read_csv(HOURLY_TRAINING_DATA)

@st.cache_data
def load_forecast_summary():
    """Loads the forecast summary results."""
    return pd.read_csv(FORECAST_SUMMARY)

def load_live_data(file_path):
    """Loads live JSON data from the scraper."""
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return None
