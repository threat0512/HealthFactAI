import streamlit as st
from components.search import render_search
from components.cards import render_fact_card
from components.sidebar import render_sidebar
from utils.api import fetch_featured_fact, get_user_progress, get_user_fact_cards
from utils.state import is_authenticated, set_page, get_user
from styles.theme import get_theme_colors

def render_quick_stats():
    """Render quick stats section with real data"""
    progress = get_user_progress()
    colors = get_theme_colors()
    
    if progress and progress.get("total_facts", 0) > 0:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(
                f"""
                <div style="background: {colors['card_bg']}; padding: 16px; border-radius: 12px; border: 1px solid {colors['border']}; text-align: center;">
                    <div style="font-size: 24px; font-weight: bold; color: {colors['accent']};">{progress['total_facts']}</div>
                    <div style="color: {colors['text_secondary']}; font-size: 14px;">Facts Learned</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                f"""
                <div style="background: {colors['card_bg']}; padding: 16px; border-radius: 12px; border: 1px solid {colors['border']}; text-align: center;">
                    <div style="font-size: 24px; font-weight: bold; color: {colors['success']};">{progress['current_streak']}</div>
                    <div style="color: {colors['text_secondary']}; font-size: 14px;">Day Streak</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col3:
            categories_count = len(progress.get("categories", {}))
            st.markdown(
                f"""
                <div style="background: {colors['card_bg']}; padding: 16px; border-radius: 12px; border: 1px solid {colors['border']}; text-align: center;">
                    <div style="font-size: 24px; font-weight: bold; color: {colors['secondary']};">{categories_count}</div>
                    <div style="color: {colors['text_secondary']}; font-size: 14px;">Categories</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)

def render_recent_activity():
    """Render recent activity section without duplicating streak info"""
    colors = get_theme_colors()
    
    # Get recent fact cards instead of just progress
    fact_cards_data = get_user_fact_cards("All", limit=3)
    
    if fact_cards_data and fact_cards_data.get("fact_cards"):
        st.markdown("### 📚 Recent Discoveries")
        
        fact_cards = fact_cards_data["fact_cards"]
        
        for i, card in enumerate(fact_cards):
            # Compact card display
            st.markdown(
                f"""
                <div style="background: {colors['card_bg']}; padding: 12px; border-radius: 8px; border: 1px solid {colors['border']}; margin-bottom: 8px;">
                    <div style="font-weight: 600; font-size: 14px; color: {colors['text']}; margin-bottom: 4px;">
                        {card.get('title', 'Health Fact')[:50]}{'...' if len(card.get('title', '')) > 50 else ''}
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="background: {colors['accent']}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">
                            {card.get('category', 'General')}
                        </span>
                        <span style="color: {colors['text_secondary']}; font-size: 11px;">
                            {card.get('confidence', 'N/A')}
                        </span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Link to see more
        if st.button("📖 View All Saved Facts", type="secondary", use_container_width=True):
            set_page("Categories")
            st.rerun()
    else:
        st.markdown("### 🚀 Get Started")
        st.info("Start searching for health topics to see your recent discoveries here!")

def render_dashboard() -> None:
    """Render the main dashboard/home page"""
    # Check if user is authenticated
    if not is_authenticated():
        set_page("Landing")
        st.rerun()
        return
    
    # Welcome message
    user = get_user()
    username = user.get("username", "User") if user else "User"
    st.markdown(f"# Welcome back, {username}! 👋")
    st.markdown("Discover, learn, and track your health knowledge journey.")
    
    # Quick stats section
    render_quick_stats()
    
    # Search functionality - now returns both query and results
    query, search_results = render_search()
    
    # Main content layout
    left, right = st.columns([2.5, 1])
    
    with left:
        # Show search results if available
        if search_results:
            st.markdown("### 🔍 Search Results")
            for i, result in enumerate(search_results):
                render_fact_card(result)
                if i < len(search_results) - 1:  # Add spacing between cards except for the last one
                    st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
        else:
            # Fetch and display featured fact when no search is active
            fact = fetch_featured_fact(query)
            render_fact_card(fact)
    
    with right:
        # Right sidebar - but remove the streak since it's now in quick stats
        render_sidebar()
        
        # Recent activity below sidebar
        render_recent_activity()