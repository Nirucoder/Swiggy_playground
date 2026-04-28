import streamlit as st
from src.config.settings import SWIGGY_ORANGE

def apply_custom_styling():
    """Applies custom CSS styling to the Streamlit app, supporting both Light and Dark modes."""
    st.markdown(f"""
        <style>
        .stButton>button {{ background-color: {SWIGGY_ORANGE}; color: white; border-radius: 8px; width: 100%; }}
        .stMetric {{ background-color: var(--secondary-background-color); padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
        .insight-card {{ background-color: var(--secondary-background-color); padding: 20px; border-radius: 12px; border-left: 5px solid {SWIGGY_ORANGE}; margin-bottom: 10px; }}
        </style>
        """, unsafe_allow_html=True)
