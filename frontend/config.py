# Frontend configuration constants
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
import streamlit as st

# Try to get from Streamlit secrets first, then environment
def get_backend_url():
    # Try Streamlit secrets first
    try:
        return st.secrets["BACKEND_API_URL"]
    except:
        pass
    
    # Try environment variable
    env_url = os.getenv("BACKEND_API_URL")
    if env_url:
        return env_url
    
    # Default to production URL
    return "https://healthfactai-1.onrender.com/api/v1"

API_URL = get_backend_url()

# Page Configuration
PAGE_TITLE = "HealthFact AI"
PAGE_ICON = "frontend/logo.jpg"  # Updated to match your file
LAYOUT = "wide"

# Color Scheme
PRIMARY = "#6366F1"    # indigo-500
ACCENT = "#10B981"     # emerald-500
SECONDARY = "#8B5CF6"  # violet-500

# Categories
CATEGORIES = ["All", "Nutrition", "Exercise", "Mental Health", "Wellness"]

# Default User (None means no user is logged in by default)
DEFAULT_USER = None