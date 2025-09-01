import streamlit as st
from styles.theme import get_theme_colors
from utils.state import set_user, set_page, is_authenticated, set_auth_token
import requests
from config import API_URL

def render_auth() -> None:
    """Render the authentication page"""
    colors = get_theme_colors()
    
    
    # If already authenticated, redirect to dashboard
    if is_authenticated():
        set_page("Home")
        st.rerun()
        return
    
    st.markdown(f"""
    <div style="text-align: center; margin: 40px 0;">
        <div style="font-size: 32px; font-weight: 800; color: {colors['text']}; margin-bottom: 8px;">Welcome Back</div>
        <div style="color: {colors['text_secondary']}; font-size: 18px;">Sign in to continue your health journey</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Center the form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("auth_form"):
            st.markdown(f"""
            <div style="background: {colors['card_bg']}; border: 1px solid {colors['border']}; border-radius: 20px; padding: 40px; margin: 20px 0;">
                <div style="font-size: 24px; font-weight: 700; margin-bottom: 32px; color: {colors['text']}; text-align: center;">Sign In</div>
            """, unsafe_allow_html=True)
            
            # Single field for username or email
            login_field = st.text_input("Username or Email", placeholder="Enter your username or email address")
            st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)  # Add spacing
            
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)  # Add spacing
            
            st.markdown(f"""
            <div style="margin-top: 32px;">
            """, unsafe_allow_html=True)
            
            ok = st.form_submit_button("Sign In", type="primary", use_container_width=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
            
            if ok:
                # Validate input
                if not login_field or not password:
                    st.error("Please enter username/email and password")
                else:
                    # Attempt to login with backend API
                    try:
                        # Use form data format for OAuth2PasswordRequestForm
                        form_data = {
                            "username": login_field,
                            "password": password
                        }
                        
                        response = requests.post(
                            f"{API_URL}/auth/login",
                            data=form_data,
                            headers={"Content-Type": "application/x-www-form-urlencoded"},
                            timeout=30  # Increased timeout for authentication
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            access_token = data.get("access_token")
                            
                            if access_token:
                                # Set token for persistent login (24 hours by default)
                                set_auth_token(access_token)
                                
                                # Set user data (we'll get more details from /me endpoint)
                                set_user({
                                    "username": login_field,
                                    "email": login_field if "@" in login_field else "",
                                    "name": "User",
                                    "role": "Health Enthusiast"
                                })
                                
                                # Try to get full user details
                                try:
                                    user_response = requests.get(
                                        f"{API_URL}/auth/me",
                                        headers={"Authorization": f"Bearer {access_token}"},
                                        timeout=20  # Increased timeout for user profile fetch
                                    )
                                    if user_response.status_code == 200:
                                        user_data = user_response.json()
                                        set_user({
                                            "id": user_data.get("id"),
                                            "username": user_data.get("username"),
                                            "email": user_data.get("email"),
                                            "name": user_data.get("name", "User"),
                                            "role": "Health Enthusiast"
                                        })
                                except Exception:
                                    # If we can't get user details, continue with basic info
                                    pass
                                
                                set_page("Home")
                                st.success("✅ Successfully signed in!")
                                st.rerun()
                            else:
                                st.error("Invalid response from server")
                        else:
                            try:
                                error_data = response.json()
                                error_detail = error_data.get("detail", "Login failed")
                                st.error(f"Login failed: {error_detail}")
                            except:
                                st.error(f"Login failed: {response.status_code}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Network error: {e}")
                    except Exception as e:
                        st.error(f"Unexpected error: {e}")
        
        # Sign up section below the form
        st.markdown(f"""
        <div style="text-align: center; margin: 20px 0;">
            <div style="color: {colors['text_secondary']}; font-size: 16px; margin-bottom: 16px;">New here?</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Center the sign up button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
                if st.button("Sign Up", key="signup-btn", use_container_width=True):
                    set_page("SignUp")
                    st.rerun()
