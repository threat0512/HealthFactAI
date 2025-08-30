import streamlit as st
import requests
from styles.theme import get_theme_colors
from utils.state import set_user, set_page
from config import API_URL


def render_signup() -> None:
    colors = get_theme_colors()

    st.markdown(f"""
    <div style="text-align:center; margin:24px 0;">
      <div style="font-size:28px; font-weight:800; color:{colors['text']};">Create your account</div>
      <div style="color:{colors['text_secondary']}; margin-top:6px;">Join HealthFactAI — verify claims, learn, and track progress</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("signup_form"):
            email = st.text_input("Email", placeholder="you@example.com")
            username = st.text_input("Username", placeholder="choose a username")
            password = st.text_input("Password", type="password", placeholder="pick a secure password")
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Sign up", type="primary", use_container_width=True)

            if submitted:
                # Basic validation
                if not email or not username or not password:
                    st.error("Please fill in all fields")
                else:
                    payload = {"email": email, "username": username, "password": password}
                    try:
                        resp = requests.post(f"{API_URL}/auth/register", json=payload, timeout=8)
                    except Exception as e:
                        st.error(f"Network error: {e}")
                        resp = None

                    if resp is not None:
                        if resp.status_code == 201:
                            data = resp.json()
                            # Set minimal user in session and navigate to welcome page
                            set_user({"id": data.get("id"), "username": data.get("username"), "email": data.get("email")})
                            st.success("Account created — welcome!")
                            set_page("Welcome")
                            st.experimental_rerun()
                        else:
                            try:
                                err = resp.json()
                                detail = err.get("detail") or err
                            except Exception:
                                detail = resp.text
                            st.error(f"Sign up failed: {detail}")
