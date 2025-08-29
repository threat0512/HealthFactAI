import streamlit as st
from styles.theme import get_theme_colors
from utils.state import set_page, is_authenticated

def render_landing() -> None:
    """Render the landing page for unauthenticated users"""
    colors = get_theme_colors()
    
    # If user is authenticated, redirect to dashboard
    if is_authenticated():
        set_page("Home")
        st.rerun()
        return
    
    # Hero section
    st.markdown(
        f"""
        <div style="text-align: center; margin: 20px 0 20px 0;">
          <div style="font-size: 48px; font-weight: 800; margin-bottom: 12px; color: {colors['text']};">
            Fight Health Misinformation
          </div>
          <div style="color: {colors['text_secondary']}; font-size: 20px; line-height: 1.4;">
            AI-powered fact-checking • Interactive learning • Trusted sources
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Features grid
    col_l, col_r = st.columns(2)
    
    with col_l:
        st.markdown(
            f"""
            <div class="hf-card">
              <div style="font-size: 20px; font-weight: 700; margin-bottom: 8px; color: {colors['text']};">Bust Health Myths</div>
              <div style="color: {colors['text_secondary']}; margin-bottom: 12px;">Separate fact from fiction with AI-powered analysis</div>
              <div style="display: flex; gap: 8px;">
                <span style="background: {colors['accent']}; color: white; padding: 6px 12px; border-radius: 999px; font-size: 12px;">Quiz</span>
                <span style="background: {colors['success']}; color: white; padding: 6px 12px; border-radius: 999px; font-size: 12px;">Learn</span>
                <span style="background: {colors['secondary']}; color: white; padding: 6px 12px; border-radius: 999px; font-size: 12px;">Track</span>
              </div>
            </div>
            <div class="hf-card">
              <div style="font-size: 20px; font-weight: 700; margin-bottom: 8px; color: {colors['text']};">Interactive Learning</div>
              <div style="color: {colors['text_secondary']}; margin-bottom: 12px;">Gamified fact-checking</div>
              <div style="display: flex; gap: 8px;">
                <span style="background: {colors['warning']}; color: white; padding: 6px 12px; border-radius: 999px; font-size: 12px;">⭐</span>
                <span style="background: {colors['success']}; color: white; padding: 6px 12px; border-radius: 999px; font-size: 12px;">✅</span>
                <span style="background: {colors['accent']}; color: white; padding: 6px 12px; border-radius: 999px; font-size: 12px;">🧠</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col_r:
        st.markdown(
            f"""
            <div class="hf-card">
              <div style="font-size: 20px; font-weight: 700; margin-bottom: 8px; color: {colors['text']};">Build Media Literacy</div>
              <div style="color: {colors['text_secondary']}; margin-bottom: 12px;">Learn to identify reliable health information sources</div>
              <div style="background: {colors['success']}; color: white; padding: 6px 12px; border-radius: 999px; font-size: 12px; display: inline-block;">
                Progress: 70%
              </div>
            </div>
            <div class="hf-card">
              <div style="font-size: 20px; font-weight: 700; margin-bottom: 8px; color: {colors['text']};">Accessible Everywhere</div>
              <div style="color: {colors['text_secondary']}; margin-bottom: 12px;">Multiple languages • Global health literacy</div>
              <div style="display: flex; gap: 8px;">
                <span style="background: {colors['accent']}; color: white; padding: 6px 12px; border-radius: 999px; font-size: 12px;">EN</span>
                <span style="background: {colors['secondary']}; color: white; padding: 6px 12px; border-radius: 999px; font-size: 12px;">ES</span>
                <span style="background: {colors['warning']}; color: white; padding: 6px 12px; border-radius: 999px; font-size: 12px;">🌐</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Single button - no extra HTML, just the button
    st.markdown("<div style='text-align: center; margin: 20px 0;'>", unsafe_allow_html=True)
    
    # Only one button here
    if st.button("Start Fact-Checking", key="landing-cta", use_container_width=True, type="primary"):
        set_page("Auth")
    
    st.markdown("</div>", unsafe_allow_html=True)
