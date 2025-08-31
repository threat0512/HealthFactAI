import streamlit as st
from styles.theme import get_theme_colors
from utils.state import clear_user, is_authenticated, get_current_page, set_page

def render_header() -> None:
    """Render the main navigation header with navigation buttons"""
    colors = get_theme_colors()
    
    # Create header with columns for better logo placement
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        # Logo using Streamlit's image function
        try:
            st.image("frontend/logo.jpg", width=40)
        except:
            # Fallback to emoji if logo not found
            st.markdown(
                f"""
                <div style="
                    background: {colors['accent']};
                    color: white;
                    width: 40px;
                    height: 40px;
                    border-radius: 8px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: 800;
                    font-size: 18px;
                ">
                    ��
                </div>
                """,
                unsafe_allow_html=True,
            )
    
    with col2:
        # Brand name
        st.markdown(
            f"""
            <div style="
                font-size: 24px;
                font-weight: 800;
                color: {colors['text']};
                text-align: center;
            ">
                HealthFactAI
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    # Navigation buttons in a single row
    nav_cols = st.columns(4, gap="small")
    
    # Home button
    with nav_cols[0]:
        current_page = get_current_page()
        is_home_active = current_page == "Home" or (current_page == "Landing" and not is_authenticated())
        
        if st.button("Home", key="nav-home", use_container_width=True, help="Go to Home page"):
            if is_authenticated():
                set_page("Home")
            else:
                set_page("Landing")
    
    # Categories button
    with nav_cols[1]:
        if st.button("Categories", key="nav-categories", use_container_width=True, help="Browse health categories"):
            set_page("Categories")
    
    # Quiz button
    with nav_cols[2]:
        if st.button("Quiz", key="nav-quiz", use_container_width=True, help="Take health quizzes"):
            if is_authenticated():
                set_page("Quiz")
                st.session_state["start_quiz"] = True
            else:
                set_page("Auth")
    
    # Progress button
    with nav_cols[3]:
        if st.button("Progress", key="nav-progress", use_container_width=True, help="View your progress"):
            set_page("Progress")
    
    # Handle button clicks
    if is_authenticated():
        if st.button("Logout", key="logout-btn", use_container_width=False):
            clear_user()
            st.rerun()
    else:
        if st.button("Sign In", key="signin-btn", use_container_width=False):
            st.session_state.page = "Auth"
            st.rerun()