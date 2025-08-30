import streamlit as st
from styles.theme import get_theme_colors
from utils.state import get_user, set_page


def render_welcome() -> None:
    colors = get_theme_colors()
    user = get_user() or {}

    st.markdown(f"""
    <div style="text-align:center; margin:40px 0;">
      <div style="font-size:32px; font-weight:800; color:{colors['text']};">Welcome, {user.get('username', 'friend')}!</div>
      <div style="color:{colors['text_secondary']}; margin-top:8px;">You're all set — start fact-checking or try a quiz to build your score.</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Start Fact-Checking", use_container_width=True, type="primary"):
            set_page("Home")
            st.experimental_rerun()
