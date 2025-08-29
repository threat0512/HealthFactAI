import streamlit as st
from styles.theme import get_theme_colors
from components.cards import render_metric_card

def render_progress() -> None:
    """Render the progress page with charts and metrics"""
    colors = get_theme_colors()
    
    st.subheader("Progress")
    
    try:
        import pandas as pd
        import plotly.express as px
        
        # Demo dataset
        progress_data = pd.DataFrame({
            "day": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
            "facts": [3,5,2,7,4,6,3],
        })
        
        # Create a better-looking chart with theme colors
        fig = px.bar(progress_data, x="day", y="facts", 
                     title="Facts Learned This Week",
                     color_discrete_sequence=[colors['accent']])
        fig.update_layout(
            plot_bgcolor=colors['card_bg'],
            paper_bgcolor=colors['card_bg'],
            font=dict(color=colors['text']),
            title_font_color=colors['text']
        )
        fig.update_xaxes(gridcolor=colors['border'], zerolinecolor=colors['border'])
        fig.update_yaxes(gridcolor=colors['border'], zerolinecolor=colors['border'])
        st.plotly_chart(fig, use_container_width=True)

        categories_data = pd.DataFrame({
            "category": ["Nutrition","Exercise","Mental Health","Wellness"],
            "count": [24,18,32,12],
        })
        pie = px.pie(categories_data, names="category", values="count", 
                     title="Learned by Category",
                     color_discrete_sequence=[colors['accent'], colors['secondary'], colors['success'], colors['warning']])
        pie.update_layout(
            plot_bgcolor=colors['card_bg'],
            paper_bgcolor=colors['card_bg'],
            font=dict(color=colors['text']),
            title_font_color=colors['text']
        )
        st.plotly_chart(pie, use_container_width=True)
        
    except Exception as ex:
        st.info("Charts unavailable. Install pandas and plotly to enable graphs.")

    # Better styled metrics
    col1, col2 = st.columns(2)
    with col1:
        render_metric_card("156", "Total Facts Learned")
    with col2:
        render_metric_card("12 days", "Current Streak")
