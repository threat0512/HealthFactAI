import streamlit as st
from typing import Dict
from styles.theme import get_theme_colors

def render_fact_card(fact: Dict) -> None:
    """Render a health fact card with styling"""
    colors = get_theme_colors()
    
    st.markdown(
        f"""
        <div class="hf-card">
          <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:16px;">
            <div style="display:flex; align-items:center; gap:12px;">
              <span class="badge badge-category">{fact.get('category', 'Nutrition')}</span>
            </div>
            <span class="badge badge-confidence">{fact.get('confidence', '92%')} confidence</span>
          </div>
          <div style="font-size:24px; font-weight:800; margin-bottom:12px; color:{colors['text']};">{fact['title']}</div>
          <div style="color:{colors['text_secondary']}; line-height:1.7; font-size:16px;">{fact['summary']}</div>
          <div style="margin-top:20px;">
            {''.join([f"<a class='source-btn' href='{s.get('url', '#')}' target='_blank'>{s.get('name', s.get('title', 'Source'))}</a>" for s in fact.get('sources', [])])}
          </div>
          <div style="display:flex; justify-content:flex-end; color:{colors['text_secondary']}; margin-top:12px; font-size:14px;">
            🔗 Share • 📖 Read More
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_info_card(title: str, description: str, badges: list = None, style: str = "default") -> None:
    """Render a general information card"""
    colors = get_theme_colors()
    
    badge_html = ""
    if badges:
        badge_html = '<div style="display: flex; gap: 8px;">'
        for badge in badges:
            badge_html += f'<span style="background: {colors["accent"]}; color: white; padding: 6px 12px; border-radius: 999px; font-size: 12px;">{badge}</span>'
        badge_html += '</div>'
    
    st.markdown(
        f"""
        <div class="hf-card">
          <div style="font-size: 20px; font-weight: 700; margin-bottom: 12px; color: {colors['text']};">{title}</div>
          <div style="color: {colors['text_secondary']}; margin-bottom: 16px;">{description}</div>
          {badge_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_metric_card(value: str, label: str) -> None:
    """Render a metric card for displaying statistics"""
    colors = get_theme_colors()
    
    st.markdown(
        f"""
        <div class="stMetric">
            <div style="font-size: 24px; font-weight: 700; color: {colors['text']};">{value}</div>
            <div style="color: {colors['text_secondary']};">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
