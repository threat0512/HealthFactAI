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
    if "access_token" not in st.session_state:
        st.session_state.access_token = None
    if "token_expires_at" not in st.session_state:
        st.session_state.token_expires_at = None
    
    # Set initial page based on authentication status
    if "page" not in st.session_state:
        if st.session_state.user and st.session_state.access_token:
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

def set_auth_token(token: str, expires_in_minutes: int = 1440):
    """Set authentication token and expiration time (default: 24 hours)"""
    import datetime
    st.session_state.access_token = token
    # Set expiration time (subtract 5 minutes for safety)
    expires_at = datetime.datetime.now() + datetime.timedelta(minutes=expires_in_minutes - 5)
    st.session_state.token_expires_at = expires_at

def get_auth_token() -> str:
    """Get current authentication token"""
    return st.session_state.get("access_token")

def is_token_valid() -> bool:
    """Check if the current token is still valid"""
    import datetime
    token = st.session_state.get("access_token")
    expires_at = st.session_state.get("token_expires_at")
    
    if not token or not expires_at:
        return False
    
    # Check if token has expired
    if datetime.datetime.now() >= expires_at:
        return False
    
    return True

def should_refresh_token() -> bool:
    """Check if token should be refreshed (within 5 minutes of expiry)"""
    import datetime
    token = st.session_state.get("access_token")
    expires_at = st.session_state.get("token_expires_at")
    
    if not token or not expires_at:
        return False
    
    # Check if token expires within 5 minutes
    refresh_time = expires_at - datetime.timedelta(minutes=5)
    return datetime.datetime.now() >= refresh_time

def get_token_info() -> dict:
    """Get debug information about the current token"""
    import datetime
    token = st.session_state.get("access_token")
    expires_at = st.session_state.get("token_expires_at")
    
    if not token or not expires_at:
        return {"status": "no_token"}
    
    now = datetime.datetime.now()
    time_until_expiry = expires_at - now
    
    return {
        "status": "valid" if is_token_valid() else "expired",
        "expires_at": expires_at.isoformat(),
        "time_until_expiry": str(time_until_expiry),
        "should_refresh": should_refresh_token(),
        "token_preview": f"{token[:10]}..." if token else None
    }

def clear_user():
    """Clear user data and tokens from session state and redirect to landing"""
    st.session_state.user = None
    st.session_state.access_token = None
    st.session_state.token_expires_at = None
    # Reset to landing page when user logs out
    st.session_state.page = "Landing"

def is_authenticated():
    """Check if user is authenticated with valid token"""
    return (st.session_state.get("user") is not None and 
            st.session_state.get("access_token") is not None and
            is_token_valid())

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
