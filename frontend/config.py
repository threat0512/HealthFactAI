# Frontend configuration constants
import os

# Try to load .env for local development (optional for Streamlit Cloud)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not available (e.g., on Streamlit Cloud) - that's fine
    pass

# API Configuration
import streamlit as st

# Try to get from Streamlit secrets first, then environment
def get_backend_url():
    # Try Streamlit secrets first
    try:
        url = st.secrets["BACKEND_API_URL"]
        print(f"[DEBUG] Using Streamlit secrets URL: {url}")
        return url
    except Exception as e:
        print(f"[DEBUG] Streamlit secrets not found: {e}")
        pass
    
    # Try environment variable
    env_url = os.getenv("BACKEND_API_URL")
    if env_url:
        print(f"[DEBUG] Using environment URL: {env_url}")
        return env_url
    
    # Default to production URL
    default_url = "https://healthfactai-1.onrender.com/api/v1"
    print(f"[DEBUG] Using default URL: {default_url}")
    return default_url

API_URL = get_backend_url()

# Page Configuration
PAGE_TITLE = "HealthFact AI"
# Handle different path structures for local vs cloud deployment
try:
    # Try relative path first (for Streamlit Cloud)
    if os.path.exists("logo.jpg"):
        PAGE_ICON = "logo.jpg"
    elif os.path.exists("frontend/logo.jpg"):
        PAGE_ICON = "frontend/logo.jpg"
    else:
        # Fallback to emoji if file not found
        PAGE_ICON = "🏥"
except:
    PAGE_ICON = "🏥"
    
LAYOUT = "wide"

# Color Scheme
PRIMARY = "#6366F1"    # indigo-500
ACCENT = "#10B981"     # emerald-500
SECONDARY = "#8B5CF6"  # violet-500

# Categories
CATEGORIES = ["All", "Nutrition", "Exercise", "Mental Health", "Wellness"]

# Default User (None means no user is logged in by default)
DEFAULT_USER = None