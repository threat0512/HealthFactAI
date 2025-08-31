# Frontend configuration constants
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
API_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000/api/v1")

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