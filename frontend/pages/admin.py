import streamlit as st
from styles.theme import get_theme_colors
from utils.state import get_claims, add_claim, update_claim
from utils.api import submit_claim as api_submit_claim, update_claim as api_update_claim

def render_admin() -> None:
    """Render the admin panel page"""
    colors = get_theme_colors()
    
    st.subheader("Admin Panel")
    st.caption("Add new misinformation claims or update explanations and trusted links.")

    # Add Claim section
    st.markdown(f"""
    <div class="hf-card" style="margin-bottom: 24px;">
        <div style="font-weight: 700; font-size: 18px; margin-bottom: 16px; color: {colors['text']};">Add New Claim</div>
    """, unsafe_allow_html=True)
    
    with st.form("add_claim_form", clear_on_submit=True):
        c_text = st.text_area("Claim text", placeholder="Enter the health claim to fact-check...")
        c_truth = st.selectbox("Verdict", ["True","False","Misleading","Unverified"])
        c_expl = st.text_area("Explanation", placeholder="Provide a detailed explanation...")
        c_source = st.text_input("Trusted source URL", placeholder="https://...")
        
        submitted = st.form_submit_button("Add Claim", type="primary")
        
        if submitted and c_text.strip():
            claim_data = {
                "claim": c_text, 
                "verdict": c_truth, 
                "explanation": c_expl, 
                "source": c_source,
            }
            
            # Add to local state
            add_claim(claim_data)
            
            # Try to submit to backend
            try:
                api_submit_claim(claim_data)
            except Exception:
                pass
            
            st.success("✅ Claim added successfully!")

    st.markdown("</div>", unsafe_allow_html=True)

    # Update Existing section
    claims = get_claims()
    if claims:
        st.markdown(f"""
        <div class="hf-card">
            <div style="font-weight: 700; font-size: 18px; margin-bottom: 16px; color: {colors['text']};">Update Existing Claims</div>
        """, unsafe_allow_html=True)
        
        options = [c["claim"][:60] + ("…" if len(c["claim"])>60 else "") for c in claims]
        idx = st.selectbox("Choose claim to update", list(range(len(options))), format_func=lambda i: options[i])
        selected = claims[idx]
        
        new_expl = st.text_area("Explanation", value=selected.get("explanation",""), key="upd_expl")
        new_src = st.text_input("Trusted source URL", value=selected.get("source",""), key="upd_src")
        
        if st.button("Update Claim", type="primary"):
            update_data = {"explanation": new_expl, "source": new_src}
            
            # Update local state
            update_claim(idx, update_data)
            
            # Try to update in backend
            try:
                api_update_claim(idx, selected)
            except Exception:
                pass
            
            st.success("✅ Claim updated successfully!")
        
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No claims available to update. Add some claims first!")
