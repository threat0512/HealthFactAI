import streamlit as st

def get_theme_colors() -> dict:
    """Get theme colors - only dark mode now"""
    return {
        "bg": "#0F172A",
        "card_bg": "#1E293B", 
        "border": "#334155",
        "text": "#F8FAFC",
        "text_secondary": "#CBD5E1",
        "accent": "#6366F1",
        "secondary": "#8B5CF6",
        "success": "#10B981",
        "warning": "#F59E0B",
        "error": "#EF4444"
    }

def initialize_theme() -> None:
    """Initialize theme - always dark mode"""
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"

def toggle_theme() -> None:
    """Theme toggle disabled - always stays dark"""
    pass
