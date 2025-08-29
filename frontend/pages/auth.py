import streamlit as st
from styles.theme import get_theme_colors
from utils.state import set_user, set_page, is_authenticated

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
                # Simple authentication - in production, you'd validate credentials
                if login_field and password:
                    # Determine if login_field is email or username
                    is_email = "@" in login_field
                    if is_email:
                        set_user({"email": login_field, "username": "", "name": "John Doe", "role": "Health Enthusiast"})
                    else:
                        set_user({"username": login_field, "email": "", "name": "John Doe", "role": "Health Enthusiast"})
                    set_page("Home")
                    st.success("✅ Successfully signed in!")
                    st.rerun()  # Force rerun to update the UI
                else:
                    st.error("Please enter username/email and password")
        
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
                st.info("🚧 Sign up functionality coming soon! We're working on it.")
                # TODO: Implement sign up page/form
                # set_page("SignUp")  # Uncomment when sign up page is ready
