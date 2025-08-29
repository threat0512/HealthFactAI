import streamlit as st
from styles.theme import get_theme_colors
from utils.state import set_page

def render_sidebar() -> None:
    """Render the right sidebar with user info and actions"""
    colors = get_theme_colors()
    
    # User profile card
    st.markdown(
        f"""
        <div class="right-card">
          <div style="display:flex; align-items:center; gap:16px;">
            <div style="width:64px; height:64px; border-radius:999px; background:linear-gradient(135deg, {colors['accent']}, {colors['secondary']}); 
                        display:flex; align-items:center; justify-content:center; font-size:28px; color:white;">🙂</div>
            <div>
              <div style="font-weight:700; font-size:18px; color:{colors['text']};">John Doe</div>
              <div style="color:{colors['text_secondary']}; font-size:14px;">Health Enthusiast</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Daily streak card
    st.markdown(
        f"""
        <div class="right-card">
          <div style="font-weight:700; margin-bottom:12px; color:{colors['text']};">Daily Streak</div>
          <div style="display:flex; align-items:center; justify-content:space-between;">
            <div style="color:{colors['text_secondary']}; font-size:16px;">🔥 12 days</div>
          </div>
          <div class="progress-bar">
            <div class="progress-fill"></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Achievements card
    st.markdown(
        f"""
        <div class="right-card">
          <div style="font-weight:700; margin-bottom:12px; color:{colors['text']};">Achievements</div>
          <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:12px;">
            <div class="hf-card" style="padding:16px; text-align:center; background:{colors['card_bg']}; border:1px solid {colors['border']};">
              🎓<div style="margin-top:8px; font-size:12px; color:{colors['text_secondary']};">Learner</div>
            </div>
            <div class="hf-card" style="padding:16px; text-align:center; background:{colors['card_bg']}; border:1px solid {colors['border']};">
              🔥<div style="margin-top:8px; font-size:12px; color:{colors['text_secondary']};">Streak</div>
            </div>
            <div class="hf-card" style="padding:16px; text-align:center; background:{colors['card_bg']}; border:1px solid {colors['border']};">
              🏆<div style="margin-top:8px; font-size:12px; color:{colors['text_secondary']};">Expert</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Daily Quiz card
    st.markdown(
        f"""
        <div class="right-card">
          <div style="font-weight:700; display:flex; align-items:center; gap:8px; margin-bottom:8px; color:{colors['text']};">
            <span>📌</span>
            <span>Daily Quiz Challenge</span>
          </div>
          <div style="color:{colors['text_secondary']}; margin-bottom:16px; font-size:14px;">
            Test your knowledge with today's health quiz!
          </div>
        """,
        unsafe_allow_html=True,
    )
    
    start = st.button("Start Quiz", key="daily_quiz_btn", help="Begin today's quiz challenge")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if start:
        st.session_state["start_quiz"] = True
        set_page("Quiz")
