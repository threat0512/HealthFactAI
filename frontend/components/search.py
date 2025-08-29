import streamlit as st
from config import CATEGORIES
from utils.state import get_active_category, set_active_category

def render_search() -> str:
    """Render the search input and category filter chips"""
    # Search input
    query = st.text_input(
        "", 
        placeholder="Ask about nutrition, exercise, mental health...", 
        label_visibility="collapsed"
    )
    
    # Category chips with better styling
    st.markdown("<div style='margin: 20px 0;'>", unsafe_allow_html=True)
    chip_cols = st.columns(len(CATEGORIES), gap="small")
    
    for idx, name in enumerate(CATEGORIES):
        with chip_cols[idx]:
            is_active = get_active_category() == name
            if st.button(
                name, 
                key=f"chip-{name}", 
                help=f"Filter by {name} category"
            ):
                set_active_category(name)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    return query
