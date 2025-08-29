import streamlit as st
from config import DEFAULT_USER, CATEGORIES

def initialize_session_state():
    """Initialize all session state variables"""
    if "active_category" not in st.session_state:
        st.session_state.active_category = "All"
    if "claims" not in st.session_state:
        st.session_state.claims = []
    if "user" not in st.session_state:
        st.session_state.user = DEFAULT_USER
    
    # Set initial page based on authentication status
    if "page" not in st.session_state:
        if st.session_state.user:
            st.session_state.page = "Home"
        else:
            st.session_state.page = "Landing"

def get_current_page():
    """Get current page from session state"""
    return st.session_state.get("page", "Landing")

def set_page(page_name: str):
    """Set current page in session state"""
    st.session_state.page = page_name

def get_active_category():
    """Get active category from session state"""
    return st.session_state.get("active_category", "All")

def set_active_category(category: str):
    """Set active category in session state"""
    st.session_state.active_category = category

def get_user():
    """Get current user from session state"""
    return st.session_state.get("user")

def set_user(user_data):
    """Set user data in session state"""
    st.session_state.user = user_data

def clear_user():
    """Clear user data from session state and redirect to landing"""
    st.session_state.user = None
    # Reset to landing page when user logs out
    st.session_state.page = "Landing"

def is_authenticated():
    """Check if user is authenticated"""
    return st.session_state.get("user") is not None

def get_claims():
    """Get claims from session state"""
    return st.session_state.get("claims", [])

def add_claim(claim_data):
    """Add a new claim to session state"""
    if "claims" not in st.session_state:
        st.session_state.claims = []
    st.session_state.claims.append(claim_data)

def update_claim(index: int, claim_data):
    """Update an existing claim in session state"""
    if "claims" in st.session_state and 0 <= index < len(st.session_state.claims):
        st.session_state.claims[index].update(claim_data)
