import streamlit as st
import os
from src.config.settings import LIVE_DATA_PATH, SCRAPER_SCRIPT
from src.utils.data_loader import load_historical_data, load_hourly_data, load_forecast_summary, load_live_data
from src.utils.weather import get_live_weather
from src.utils.styles import apply_custom_styling
from src.components.forecasting_tab import render_forecasting_tab
from src.components.behavior_tab import render_behavior_tab

# Set Page Config
st.set_page_config(page_title="Swiggy Demand Predictor", page_icon="🍔", layout="wide")

# Apply Styling
apply_custom_styling()

# Load Data & Weather
df_history = load_historical_data()
df_hourly = load_hourly_data()
df_summary = load_forecast_summary()
weather = get_live_weather()

# Sidebar: Live Scraper
# Swiggy logo removed due to broken link
st.sidebar.title("Live Scraper Feed")

if st.sidebar.button("Run Live Swiggy Scraper"):
    with st.sidebar.status("Scraping Swiggy Live...", expanded=True):
        # Note: Ensure the script path is correct relative to the execution root
        os.system(f"python {SCRAPER_SCRIPT}")
        st.success("Scrape Complete!")

live_json = load_live_data(LIVE_DATA_PATH)
if live_json:
    st.sidebar.info(f"Tracked: {live_json.get('restaurant', 'N/A')}")
    st.sidebar.metric("Live Sentiment", f"{live_json.get('live_sentiment_score', 0)}")

# Main Dashboard
st.title("Swiggy Demand Forecasting Dashboard")

# Navigation Tabs
tab1, tab2 = st.tabs(["Forecasting", "Customer Behavior & Trends"])

with tab1:
    selected_cat, selected_display = render_forecasting_tab(df_history, df_hourly, df_summary, weather)

with tab2:
    render_behavior_tab(df_history, selected_cat, selected_display)
