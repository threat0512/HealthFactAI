import streamlit as st
from styles.theme import get_theme_colors
from utils.state import set_page, get_user

def render_sidebar() -> None:
    """Render the right sidebar with user info and actions"""
    colors = get_theme_colors()
    
    # Get user info
    user = get_user()
    username = user.get("username", "User") if user else "User"
    
    # User profile card with real username
    st.markdown(
        f"""
        <div class="right-card">
          <div style="display:flex; align-items:center; gap:16px;">
            <div style="width:64px; height:64px; border-radius:999px; background:linear-gradient(135deg, {colors['accent']}, {colors['secondary']}); 
                        display:flex; align-items:center; justify-content:center; font-size:28px; color:white;">
              {username[0].upper() if username else 'U'}
            </div>
            <div>
              <div style="font-weight:700; font-size:18px; color:{colors['text']};">{username}</div>
              <div style="color:{colors['text_secondary']}; font-size:14px;">Health Enthusiast</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Quick actions card
    st.markdown(
        f"""
        <div class="right-card">
          <div style="font-weight:700; margin-bottom:16px; color:{colors['text']};">Quick Actions</div>
          <div style="display: flex; flex-direction: column; gap: 8px;">
        """,
        unsafe_allow_html=True,
    )
    
    # Quick action buttons
    if st.button("📊 View Progress", type="secondary", use_container_width=True, key="sidebar_progress"):
        set_page("Progress")
        st.rerun()
    
    if st.button("🧠 Take Quiz", type="secondary", use_container_width=True, key="sidebar_quiz"):
        set_page("Quiz")
        st.rerun()
    
    if st.button("📚 Browse Categories", type="secondary", use_container_width=True, key="sidebar_categories"):
        set_page("Categories")
        st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)

    # Hardcoded Achievements card (as requested)
    st.markdown(
        f"""
        <div class="right-card">
          <div style="font-weight:700; margin-bottom:16px; color:{colors['text']};">🏆 Achievements</div>
          <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:12px;">
            <div style="padding:16px; text-align:center; background:{colors['card_bg']}; border:1px solid {colors['border']}; border-radius: 8px;">
              <div style="font-size: 24px; margin-bottom: 4px;">🎓</div>
              <div style="font-size: 12px; color:{colors['text_secondary']};">First Steps</div>
              <div style="font-size: 10px; color:{colors['success']};">✅ Completed</div>
            </div>
            <div style="padding:16px; text-align:center; background:{colors['card_bg']}; border:1px solid {colors['border']}; border-radius: 8px;">
              <div style="font-size: 24px; margin-bottom: 4px;">🔥</div>
              <div style="font-size: 12px; color:{colors['text_secondary']};">Streak Master</div>
              <div style="font-size: 10px; color:{colors['success']};">✅ Completed</div>
            </div>
            <div style="padding:16px; text-align:center; background:{colors['card_bg']}; border:1px solid {colors['border']}; border-radius: 8px;">
              <div style="font-size: 24px; margin-bottom: 4px;">🏆</div>
              <div style="font-size: 12px; color:{colors['text_secondary']};">Knowledge Seeker</div>
              <div style="font-size: 10px; color:{colors['warning']};">🔄 In Progress</div>
            </div>
            <div style="padding:16px; text-align:center; background:{colors['card_bg']}; border:1px solid {colors['border']}; border-radius: 8px;">
              <div style="font-size: 24px; margin-bottom: 4px;">🌟</div>
              <div style="font-size: 12px; color:{colors['text_secondary']};">Health Expert</div>
              <div style="font-size: 10px; color:{colors['text_secondary']};">🔒 Locked</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Learning tip card
    st.markdown(
        f"""
        <div class="right-card">
          <div style="font-weight:700; margin-bottom:12px; color:{colors['text']};">💡 Daily Tip</div>
          <div style="color:{colors['text_secondary']}; font-size: 14px; line-height: 1.4;">
            Regular physical activity can improve your mood and reduce stress levels. Even a 10-minute walk can make a difference!
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )