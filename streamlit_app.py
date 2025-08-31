"""
Streamlit Cloud entry point for HealthFact AI
"""
import sys
import os

# Add frontend directory to Python path for proper imports
frontend_path = os.path.join(os.path.dirname(__file__), 'frontend')
sys.path.insert(0, frontend_path)

# Change working directory to frontend for relative imports
os.chdir(frontend_path)

# Now run the main app
exec(open('app.py').read())
