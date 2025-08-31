

def generate_css():
    """Legacy function - kept for compatibility but not used"""
    return ""


def generate_dynamic_css(colors: dict) -> str:
    """Generate dynamic CSS for components based on theme colors"""
    return f"""
        /* Base theme - dark mode only */
        .stApp {{
            background: {colors['bg']};
            color: {colors['text']};
        }}
        
        /* Streamlit buttons styling */
        .stButton > button {{
            background: {colors['card_bg']} !important;
            border: 2px solid {colors['border']} !important;
            color: {colors['text']} !important;
            border-radius: 12px !important;
            height: 44px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
        }}
        
        .stButton > button:hover {{
            border-color: {colors['accent']} !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3) !important;
        }}
        
        /* Primary button styling */
        .stButton > button[data-baseweb="button"] {{
            background: {colors['accent']} !important;
            border-color: {colors['accent']} !important;
            color: white !important;
        }}
        
        .stButton > button[data-baseweb="button"]:hover {{
            background: #4F46E5 !important;
            border-color: #4F46E5 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4) !important;
        }}
        
        /* Form inputs styling */
        .stTextInput input {{
            background: {colors['card_bg']} !important;
            border: 2px solid {colors['border']} !important;
            color: {colors['text']} !important;
            border-radius: 8px !important;
            padding: 12px 16px !important;
        }}
        
        .stTextInput input:focus {{
            border-color: {colors['accent']} !important;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
        }}
        
        /* Placeholder text styling */
        .stTextInput input::placeholder {{
            color: {colors['text_secondary']} !important;
            opacity: 1 !important;
        }}
        
        /* General input styling */
        input[type="text"], input[type="password"], input[type="email"], textarea {{
            background: {colors['card_bg']} !important;
            border: 2px solid {colors['border']} !important;
            color: {colors['text']} !important;
            border-radius: 8px !important;
            padding: 12px 16px !important;
        }}
        
        input[type="text"]::placeholder, input[type="password"]::placeholder, 
        input[type="email"]::placeholder, textarea::placeholder {{
            color: {colors['text_secondary']} !important;
            opacity: 1 !important;
        }}
        
        /* Card styling */
        .hf-card {{
            background: {colors['card_bg']};
            border: 1px solid {colors['border']};
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            transition: all 0.2s ease;
        }}
        
        .hf-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
            border-color: {colors['accent']};
        }}
        
        /* Search results styling */
        .search-results {{
            margin-top: 20px;
            padding: 20px;
            background: {colors['card_bg']};
            border-radius: 16px;
            border: 1px solid {colors['border']};
        }}
        
        /* Loading animation */
        .loading-container {{
            text-align: center;
            padding: 40px 20px;
        }}
        
        /* Progress bar styling */
        .stProgress > div > div > div > div {{
            background-color: {colors['accent']} !important;
        }}
        
        /* Status text styling */
        .status-text {{
            color: {colors['text_secondary']};
            font-size: 16px;
            margin: 10px 0;
            text-align: center;
        }}
        
        /* Success/Info message styling */
        .stSuccess, .stInfo {{
            border-radius: 12px !important;
            border: 2px solid !important;
        }}
        
        .stSuccess {{
            border-color: #10B981 !important;
            background-color: rgba(16, 185, 129, 0.1) !important;
        }}
        
        .stInfo {{
            border-color: #3B82F6 !important;
            background-color: rgba(59, 130, 246, 0.1) !important;
        }}
        
        /* Navigation buttons */
        .nav-btn {{
            background: {colors['card_bg']} !important;
            border: 2px solid {colors['border']} !important;
            color: {colors['text']} !important;
            border-radius: 12px !important;
            padding: 12px 24px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
            cursor: pointer !important;
        }}
        
        .nav-btn:hover {{
            border-color: {colors['accent']} !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3) !important;
        }}
        
        /* Category chips */
        .category-chip {{
            background: {colors['card_bg']} !important;
            border: 2px solid {colors['border']} !important;
            color: {colors['text']} !important;
            border-radius: 999px !important;
            padding: 8px 16px !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
            cursor: pointer !important;
            display: inline-block !important;
            margin: 4px !important;
        }}
        
        .category-chip:hover {{
            border-color: {colors['accent']} !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3) !important;
        }}
        
        /* Button spacing and layout */
        button {{
            margin: 4px !important;
            position: relative !important;
            z-index: 1 !important;
            display: inline-block !important;
            vertical-align: middle !important;
        }}
        
        .stButton {{
            margin: 4px !important;
            position: relative !important;
            z-index: 1 !important;
            display: inline-block !important;
            vertical-align: middle !important;
        }}
        
        div[data-testid="stButton"] {{
            margin: 4px !important;
            position: relative !important;
            z-index: 1 !important;
            display: inline-block !important;
            vertical-align: middle !important;
        }}
    """

