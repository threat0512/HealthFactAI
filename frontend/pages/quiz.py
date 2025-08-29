import streamlit as st
from utils.api import check_health_claim, fetch_quiz_questions, search_and_verify_claim, get_user_progress

def save_fact_for_user(**kwargs):
    """Placeholder function - progress is tracked automatically via API"""
    pass

def show_recent_facts(limit=6):
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

def render_quiz() -> None:
    """Render the quiz page with health claim checker and quiz mode"""
    
    # Health Claim Checker
    with st.expander("Check a Health Claim"):
        claim = st.text_area("Enter a health claim:")
        if st.button("Check Claim") and claim.strip():
            result = search_and_verify_claim(claim)
            if result:
                if result.get("is_verified"):
                    st.success("✅ Claim verified!")
                else:
                    st.warning("⚠️ Claim could not be verified")
                st.write(f"Explanation: {result.get('explanation', 'No explanation available')}")
                sources = result.get("sources", [])
                if sources and sources[0].get("url"):
                    st.markdown(f"[Trusted Source]({sources[0]['url']})")
                # Offer to save verified claim to user's profile
                save_fact_for_user(
                    content=claim,
                    category="claim-check",
                    source_url=sources[0].get("url") if sources else None,
                    button_label="✅ I learned this fact!",
                )
            else:
                st.error("Error connecting to backend or invalid claim.")

    # Quiz Mode
    with st.expander("Quiz Mode", expanded=st.session_state.get("start_quiz", False)):
        start_clicked = st.button("Start Quiz") or st.session_state.get("start_quiz", False)
        
        if start_clicked:
            questions = fetch_quiz_questions()
            
            if questions:
                for q in questions:
                    st.write(q.get("question", ""))
                    answer = st.radio("Your answer:", q.get("options", []), key=q.get("id", "q"))
                    
                    if st.button(f"Submit {q.get('id', '')}"):
                        if answer == q.get("answer"):
                            st.write("✅ Correct!")
                        else:
                            st.write("❌ Wrong")
            else:
                st.error("Could not fetch quiz questions. Backend may be unavailable.")

            # Reset quiz flag after rendering
            if st.session_state.get("start_quiz"):
                st.session_state["start_quiz"] = False

    # Recent facts after interactions
    show_recent_facts(limit=6)
