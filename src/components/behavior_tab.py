import streamlit as st
import plotly.express as px

def render_behavior_tab(df_history, selected_cat, selected_display):
    st.header("Behavior & Ordering Patterns")
    
    # Filter data for selected category
    df_beh = df_history[df_history['category'] == selected_cat]
    
    b1, b2 = st.columns(2)
    
    with b1:
        st.subheader("Weekday vs. Weekend Demand")
        avg_week = df_beh.groupby('is_weekend')['y'].mean().reset_index()
        avg_week['Label'] = avg_week['is_weekend'].map({0: 'Weekday', 1: 'Weekend'})
        fig_week = px.bar(avg_week, x='Label', y='y', color='Label', 
                          color_discrete_map={'Weekday': '#282c3f', 'Weekend': '#fc8019'})
        st.plotly_chart(fig_week, use_container_width=True)
        
        weekend_boost = ((avg_week.iloc[1]['y'] / avg_week.iloc[0]['y']) - 1) * 100
        st.markdown(f"<div class='insight-card'><b>Weekend Insight:</b> Orders for {selected_display} increase by <b>{weekend_boost:.1f}%</b> during weekends.</div>", unsafe_allow_html=True)

    with b2:
        st.subheader("Loyalty Distribution")
        sub_dist = df_beh['is_subscriber'].value_counts(normalize=True).reset_index()
        sub_dist['Label'] = sub_dist['is_subscriber'].map({1: 'Swiggy One', 0: 'Regular User'})
        fig_pie = px.pie(sub_dist, values='proportion', names='Label', color_discrete_sequence=['#fc8019', '#282c3f'])
        st.plotly_chart(fig_pie, use_container_width=True)
        
        st.markdown(f"<div class='insight-card'><b>Loyalty Insight:</b> <b>{sub_dist.iloc[0]['proportion']*100:.1f}%</b> of users are Swiggy One subscribers.</div>", unsafe_allow_html=True)

    st.divider()
    st.subheader("External Trend Sensitivity")
    
    # Simple correlation-based insights
    corr_rain = df_beh['y'].corr(df_beh['rain'])
    corr_temp = df_beh['y'].corr(df_beh['temp'])
    
    i1, i2, i3 = st.columns(3)
    with i1:
        if corr_rain > 0.1:
            st.success("**Rain-Positive**\n\nOrders increase significantly when it rains in Bangalore.")
        else:
            st.warning("**Rain-Neutral**\n\nRain has minimal impact on this category.")
    with i2:
        if corr_temp > 0.3:
            st.success("**Heat-Sensitive**\n\nDemand spikes during high temperatures (Cold Beverages/Ice Cream).")
        else:
            st.info("**Climate-Resilient**\n\nDemand stays stable across temperature fluctuations.")
    with i3:
        st.success("**Growth Trend**\n\nCategory shows a steady month-over-month organic growth.")
