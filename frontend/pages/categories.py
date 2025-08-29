import streamlit as st
from components.search import render_search
from styles.theme import get_theme_colors
from utils.state import get_active_category

def render_categories() -> None:
    """Render the categories page"""
    colors = get_theme_colors()
    
    st.subheader("Browse Categories")
    
    # Search functionality
    _ = render_search()
    
    # Better styled active category indicator
    st.markdown(f"""
    <div style="background: {colors['accent']}; color: white; padding: 16px; border-radius: 16px; text-align: center; margin: 20px 0;">
        <div style="font-weight: 700; font-size: 18px;">Active Category</div>
        <div style="font-size: 24px; margin-top: 8px;">{get_active_category()}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # You can add more category-specific content here
    st.info("Category-specific content will be displayed here based on the selected category.")
