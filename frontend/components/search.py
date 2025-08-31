import streamlit as st
from config import CATEGORIES
from utils.state import get_active_category, set_active_category, is_authenticated, set_page
from utils.api import search_health_claims, track_search_activity

def render_search() -> tuple[str, list]:
    """Render the search input, category filter chips, and handle search functionality"""
    # Search input with button - better alignment
    st.markdown("""
        <style>
        .search-container {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .search-input {
            flex: 1;
        }
        .search-button {
            flex-shrink: 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Use CSS flexbox for perfect alignment
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    # Search input
    query = st.text_input(
        "", 
        placeholder="Ask about nutrition, exercise, mental health...", 
        label_visibility="collapsed",
        key="search_input"
    )
    
    # Search button
    search_button = st.button("🔍 Search", type="primary")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Category chips with better styling
    st.markdown("<div style='margin: 20px 0;'>", unsafe_allow_html=True)
    chip_cols = st.columns(len(CATEGORIES), gap="small")
    
    for idx, name in enumerate(CATEGORIES):
        with chip_cols[idx]:
            is_active = get_active_category() == name
            if st.button(
                name, 
                key=f"chip-{name}", 
                help=f"Filter by {name} category"
            ):
                set_active_category(name)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Search functionality
    search_results = []
    if (query and len(query.strip()) > 0) and search_button:
        # Check if user is authenticated
        if not is_authenticated():
            st.error("🔐 Please log in to search for health information.")
            return query, search_results
        
        # Simple loading state
        with st.spinner("🔍 Searching..."):
            results = search_health_claims(query.strip())
        
        # Show results
        if results:
            search_results = results
            st.success(f"✅ Found {len(results)} result(s) for '{query}'")
            
            # Track search activity in background
            track_search_activity(query.strip())
        else:
            st.info(f"🔍 No results found for '{query}'. Try rephrasing your question.")
    
    return query, search_results
