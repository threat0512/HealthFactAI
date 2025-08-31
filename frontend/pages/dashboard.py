import streamlit as st
from components.search import render_search
from components.cards import render_fact_card
from components.sidebar import render_sidebar
from utils.api import fetch_featured_fact, get_user_progress
from utils.state import is_authenticated, set_page, get_token_info, get_user

def save_fact_for_user(**kwargs):
    """Placeholder function - progress is tracked automatically via API"""
    pass

def show_recent_facts(limit=8):
    """Show recent facts using progress API"""
    progress = get_user_progress()
    if progress and progress.get("total_facts", 0) > 0:
        st.markdown("### 📚 Your Recent Facts")
        st.metric("Total Facts Learned", progress["total_facts"])
        st.metric("Current Streak", progress["current_streak"])
        if progress.get("categories"):
            st.write("**Categories:**")
            for category, count in progress["categories"].items():
                st.write(f"- {category}: {count} facts")
    else:
        st.info("Start searching for health facts to see your progress here!")

def render_dashboard() -> None:
    """Render the main dashboard/home page"""
    # Check if user is authenticated
    if not is_authenticated():
        set_page("Landing")
        st.rerun()
        return

    
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
                st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
        else:
            # Fetch and display featured fact when no search is active
            fact = fetch_featured_fact(query)
            render_fact_card(fact)
            # Save fact button (integrated with FastAPI)
            save_fact_for_user(
                content=fact.get("title", ""),
                category=fact.get("category", "general"),
                source_url=(fact.get("sources") or [{}])[0].get("url"),
            )
    
    with right:
        # Right sidebar
        render_sidebar()
        # Recent facts list below sidebar widgets
        show_recent_facts(limit=8)
