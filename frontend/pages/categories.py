import streamlit as st
from typing import Dict, List
from components.cards import render_fact_card
from styles.theme import get_theme_colors
from utils.state import get_active_category, set_active_category, is_authenticated
from utils.api import get_user_fact_cards, get_fact_card_categories, search_fact_cards, delete_fact_card

def render_category_filter(categories: List[str]) -> str:
    """Render category filter chips and return selected category."""
    colors = get_theme_colors()
    
    st.markdown("### 🏷️ Filter by Category")
    
    # Create columns for category chips
    if len(categories) <= 5:
        chip_cols = st.columns(len(categories))
    else:
        # If more than 5 categories, use multiple rows
        chip_cols = st.columns(5)
    
    selected_category = get_active_category()
    
    for idx, category in enumerate(categories):
        col_idx = idx % len(chip_cols)
        with chip_cols[col_idx]:
            is_active = selected_category == category
            
            # Use different styling for active category
            button_type = "primary" if is_active else "secondary"
            
            if st.button(
                category, 
                key=f"category_chip_{category}",
                type=button_type,
                use_container_width=True,
                help=f"Show fact cards in {category} category"
            ):
                set_active_category(category)
                st.rerun()
    
    return selected_category

def render_fact_card_grid(fact_cards: List[Dict], show_delete: bool = True):
    """Render fact cards in a grid layout."""
    if not fact_cards:
        st.info("📭 No fact cards found in this category. Start searching to save fact cards!")
        return
    
    # Display fact cards in a grid (2 columns)
    for i in range(0, len(fact_cards), 2):
        col1, col2 = st.columns(2)
        
        # First card
        if i < len(fact_cards):
            with col1:
                card = fact_cards[i]
                render_fact_card(card)
                
                # Add delete button if enabled
                if show_delete and card.get("id"):
                    if st.button(f"🗑️ Delete", key=f"delete_{card['id']}", type="secondary"):
                        if delete_fact_card(card["id"]):
                            st.success("✅ Fact card deleted!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to delete fact card")
        
        # Second card
        if i + 1 < len(fact_cards):
            with col2:
                card = fact_cards[i + 1]
                render_fact_card(card)
                
                # Add delete button if enabled
                if show_delete and card.get("id"):
                    if st.button(f"🗑️ Delete", key=f"delete_{card['id']}", type="secondary"):
                        if delete_fact_card(card["id"]):
                            st.success("✅ Fact card deleted!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to delete fact card")

def render_search_within_cards():
    """Render search functionality within saved fact cards."""
    st.markdown("### 🔍 Search Your Saved Facts")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "",
            placeholder="Search within your saved fact cards...",
            label_visibility="collapsed",
            key="fact_card_search"
        )
    
    with col2:
        search_button = st.button("🔍 Search Facts", type="primary", use_container_width=True)
    
    if search_button and search_query.strip():
        active_category = get_active_category()
        search_category = None if active_category == "All" else active_category
        
        with st.spinner("🔍 Searching your fact cards..."):
            search_results = search_fact_cards(search_query.strip(), search_category)
        
        if search_results:
            st.success(f"✅ Found {len(search_results)} matching fact card(s)")
            st.markdown("#### 📋 Search Results")
            render_fact_card_grid(search_results)
        else:
            st.info(f"🔍 No fact cards found matching '{search_query}' in {active_category} category.")
        
        return True  # Indicates search was performed
    
    return False  # No search performed

def render_categories() -> None:
    """Render the categories page with saved fact cards."""
    if not is_authenticated():
        st.error("🔐 Please log in to view your saved fact cards.")
        return
    
    colors = get_theme_colors()
    
    st.subheader("📚 Your Saved Fact Cards")
    
    # Load user's saved fact cards
    with st.spinner("📚 Loading your saved fact cards..."):
        categories = get_fact_card_categories()
    
    if not categories or (len(categories) == 1 and categories[0] == "All"):
        st.info("""
        📭 **No saved fact cards yet!**
        
        Start searching for health topics to automatically save fact cards. 
        Your searches will be organized by categories for easy browsing.
        """)
        return
    
    # Category filter
    selected_category = render_category_filter(categories)
    
    st.markdown("---")
    
    # Search within saved fact cards
    search_performed = render_search_within_cards()
    
    # Only show all fact cards if no search was performed
    if not search_performed:
        st.markdown(f"#### 📋 Saved Facts - {selected_category}")
        
        # Load fact cards for selected category
        with st.spinner(f"📚 Loading {selected_category} fact cards..."):
            fact_cards_data = get_user_fact_cards(selected_category, limit=50)
        
        if fact_cards_data:
            fact_cards = fact_cards_data.get("fact_cards", [])
            total_count = fact_cards_data.get("total_count", 0)
            
            if fact_cards:
                # Show stats
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📊 Total Cards", total_count)
                with col2:
                    st.metric("🏷️ Category", selected_category)
                with col3:
                    if fact_cards_data.get("has_more", False):
                        st.metric("📄 Showing", f"{len(fact_cards)} of {total_count}")
                    else:
                        st.metric("📄 Cards", len(fact_cards))
                
                st.markdown("---")
                
                # Render fact cards
                render_fact_card_grid(fact_cards)
                
                # Pagination info
                if fact_cards_data.get("has_more", False):
                    st.info(f"📄 Showing first {len(fact_cards)} cards. More cards available - use search to find specific topics.")
            else:
                st.info(f"📭 No fact cards found in {selected_category} category.")
        else:
            st.error("❌ Could not load fact cards. Please try again later.")
    
    # Tips and information
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.info("""
    🏷️ **Use category filters** to organize your knowledge by health topics
    
    🔎 **Search within saved facts** to quickly find specific information
    
    🗑️ **Delete cards** you no longer need to keep your collection organized
    
    💡 **New fact cards are automatically saved** when you search from the Home page
    """)