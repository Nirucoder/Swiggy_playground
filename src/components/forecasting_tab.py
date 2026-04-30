import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import pickle
import os
from datetime import timedelta
from src.config.settings import MODELS_DIR

def render_forecasting_tab(df_history, df_hourly, df_summary, weather):
    # --- Row 1: The Best Seller Focus ---
    st.subheader("🏆 Next Month's Champion")
    winner_raw = df_summary.iloc[0]['category']
    winner_display = winner_raw
    for p in ['Indian ', 'Italian ', 'Thai ', 'Continental ']:
        winner_display = winner_display.replace(p, '')

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    
    monthly_orders = df_summary.iloc[0]['predicted_30day_orders']
    weekly_forecast = monthly_orders // 4
    hourly_champ = df_hourly[df_hourly['category'] == winner_raw].groupby('hour')['y'].mean().reset_index()
    champ_peak_hour = int(hourly_champ.loc[hourly_champ['y'].idxmax(), 'hour'])

    with c1: st.metric("Top Product", winner_display)
    with c2: st.metric("Monthly Forecast", f"{monthly_orders:,}")
    with c3: st.metric("Weekly Forecast", f"{weekly_forecast:,}")
    with c4: st.metric("Peak Hour", f"{champ_peak_hour}:00")
    with c5: st.metric("Live Temp", f"{weather['temp']}°C")
    with c6: st.metric("Live Rain", f"{weather['rain']}mm")

    st.divider()

    # --- Simulation Lab ---
    st.subheader("🧪 'What-If' Simulation Laboratory")
    sc1, sc2, sc3, sc4 = st.columns(4)
    with sc1: in_temp = st.slider("Temperature (C)", 15, 45, int(weather['temp']))
    with sc2: in_rain = st.slider("Rainfall (mm)", 0, 100, int(weather['rain']))
    with sc3: in_sent = st.slider("Public Sentiment", -1.0, 1.0, 0.2)
    with sc4: in_discount = st.slider("Active Discount (%)", 0, 60, 0)

    st.divider()

    # Row 2: Charts
    col_left, col_right = st.columns([2, 1])

    with col_left:
        selected_display = st.selectbox("Select Product to Analyze:", df_history['display_name'].unique(), index=4)
        selected_cat = df_history[df_history['display_name'] == selected_display]['category'].iloc[0]
        
        model_filename = f"{selected_cat.lower().replace(' ', '_')}.pkl"
        model_path = os.path.join(MODELS_DIR, model_filename)
        
        if os.path.exists(model_path):
            with open(model_path, "rb") as f:
                m = pickle.load(f)
            
            future_dates = pd.date_range(start=df_history['ds'].max() + timedelta(days=1), periods=30)
            future = pd.DataFrame({'ds': future_dates})
            future['temp'] = in_temp
            future['rain'] = in_rain
            future['sentiment_lag_7'] = in_sent
            future['discount'] = in_discount
            future['is_subscriber'] = 0.5
            
            forecast = m.predict(future)
            # Visual boost for demo
            discount_impact = (in_discount / 100) * 0.8
            forecast['yhat'] = forecast['yhat'] * (1 + discount_impact)

            fig = go.Figure()
            hist_data = df_history[df_history['category'] == selected_cat]
            fig.add_trace(go.Scatter(x=hist_data['ds'].tail(60), y=hist_data['y'].tail(60), name="Historical", line=dict(color='#282c3f', width=2)))
            fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], name="AI Prediction", line=dict(color='#fc8019', width=4)))
            fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=20, b=0), height=400, hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"Model for {selected_cat} not found at {model_path}")

    with col_right:
        st.subheader("⏰ Hourly Peaks")
        hourly_pattern = df_hourly[df_hourly['category'] == selected_cat].groupby('hour')['y'].mean().reset_index()
        hourly_pattern['percentage'] = (hourly_pattern['y'] / hourly_pattern['y'].sum()) * 100
        fig_hourly = px.bar(hourly_pattern, x='hour', y='percentage', color_discrete_sequence=['#fc8019'])
        fig_hourly.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=10, b=0), height=300)
        st.plotly_chart(fig_hourly, use_container_width=True)
        peak_hour = hourly_pattern.loc[hourly_pattern['percentage'].idxmax(), 'hour']
        st.info(f"**Peak:** {int(peak_hour)}:00")
    
    return selected_cat, selected_display
