import streamlit as st
from components.search import render_search
from components.cards import render_fact_card
from components.sidebar import render_sidebar
from utils.api import fetch_featured_fact
from utils.state import is_authenticated, set_page

def render_dashboard() -> None:
    """Render the main dashboard/home page"""
    # Check if user is authenticated
    if not is_authenticated():
        set_page("Landing")
        st.rerun()
        return
    
    # Search functionality
    query = render_search()
    
    # Main content layout
    left, right = st.columns([2.5, 1])
    
    with left:
        # Fetch and display featured fact
        fact = fetch_featured_fact(query)
        render_fact_card(fact)
    
    with right:
        # Right sidebar
        render_sidebar()
