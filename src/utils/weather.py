import requests
import streamlit as st
from src.config.settings import WEATHER_API_KEY

@st.cache_data(ttl=3600)
def get_live_weather(city="Bangalore"):
    """Fetches live weather data from WeatherAPI."""
    url = f"http://api.weatherapi.com/1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no"
    try:
        response = requests.get(url)
        data = response.json()
        return {
            "temp": data['current']['temp_c'],
            "rain": data['current']['precip_mm'],
            "condition": data['current']['condition']['text']
        }
    except Exception as e:
        # Fallback to default weather
        return {"temp": 28.0, "rain": 0.0, "condition": "Cloudy"}
