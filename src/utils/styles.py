import streamlit as st
from src.config.settings import SWIGGY_ORANGE, SWIGGY_DARK, BACKGROUND_COLOR

def apply_custom_styling():
    """Applies custom CSS styling to the Streamlit app."""
    st.markdown(f"""
        <style>
        .main {{ background-color: {BACKGROUND_COLOR}; }}
        .stButton>button {{ background-color: {SWIGGY_ORANGE}; color: white; border-radius: 8px; width: 100%; }}
        .stMetric {{ background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
        .insight-card {{ background-color: #fff; padding: 20px; border-radius: 12px; border-left: 5px solid {SWIGGY_ORANGE}; margin-bottom: 10px; }}
        h1, h2, h3 {{ color: {SWIGGY_DARK}; }}
        </style>
        """, unsafe_allow_html=True)
