import streamlit as st

# Import our modular components
from config import PAGE_TITLE, PAGE_ICON, LAYOUT
from styles.theme import initialize_theme
from styles.components import generate_dynamic_css
from utils.state import initialize_session_state, get_current_page, is_authenticated, is_token_valid, should_refresh_token, clear_user
from components.header import render_header
from pages.landing import render_landing
from pages.auth import render_auth
from pages.signup import render_signup
from pages.welcome import render_welcome
from pages.dashboard import render_dashboard
from pages.categories import render_categories
from pages.quiz import render_quiz
from pages.progress import render_progress


# Page configuration
st.set_page_config(
    page_title=PAGE_TITLE, 
    page_icon=PAGE_ICON, 
    layout=LAYOUT
)

# Initialize session state and theme
initialize_session_state()
initialize_theme()

# Apply CSS with current theme colors
from styles.theme import get_theme_colors
colors = get_theme_colors()
css = generate_dynamic_css(colors)
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# Render header
render_header()

# Check token validity and handle expired tokens
if st.session_state.get("user") and st.session_state.get("access_token"):
    if not is_token_valid():
        # Token has expired, clear user and redirect to auth
        clear_user()
        st.rerun()
    elif should_refresh_token():
        # Token is about to expire, show warning
        st.warning("🔑 Your session will expire soon. Please save your work.")

# Main page routing
current_page = get_current_page()

if current_page == "Landing":
    render_landing()
elif current_page == "Auth":
    render_auth()
elif current_page == "SignUp":
    render_signup()
elif current_page == "Welcome":
    render_welcome()
elif current_page == "Home":
    render_dashboard()
elif current_page == "Categories":
    render_categories()
elif current_page == "Quiz":
    render_quiz()
elif current_page == "Progress":
    render_progress()

else:
    # Default to landing page
    render_landing()
