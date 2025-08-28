import streamlit as st
import requests
from typing import List, Dict

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="HealthFact AI", page_icon="🧠", layout="wide")

# ------------------------------
# Theme & CSS helpers
# ------------------------------
PRIMARY = "#10B981"  # emerald
ACCENT = "#60A5FA"   # blue-400

CUSTOM_CSS = f"""
<style>
/* Base */
.stApp {{
    background: #0B0F12;
    color: #E5E7EB;
}}

/* Header bar */
.hf-header {{
    display: flex; align-items: center; justify-content: space-between;
    background: #0F1418; border: 1px solid #1F2937; border-radius: 16px;
    padding: 12px 16px; margin-bottom: 16px;
}}
.hf-brand {{ display:flex; align-items:center; gap:12px; font-weight:700; }}
.hf-logo {{
    width: 36px; height: 36px; border-radius: 10px; background: #111827;
    display:flex; align-items:center; justify-content:center; border:1px solid #1F2937;
}}
.hf-nav a {{ color: #9CA3AF; margin: 0 12px; text-decoration: none; }}
.hf-nav a.active {{ color: #FFF; }}
.hf-actions .btn {{
    padding: 8px 14px; border-radius: 10px; border: 1px solid #1F2937; margin-left: 8px;
}}
.btn-primary {{ background: {PRIMARY}; color:#04120D; border: none; }}

/* Search bar */
.hf-search {{
    background:#0F1418; border:1px solid #1F2937; border-radius:14px; padding:10px 12px;
    display:flex; align-items:center; gap:10px; margin-bottom:12px;
}}
.hf-search input {{
    background: transparent; border: none; outline: none; color: #E5E7EB; width: 100%;
}}
.hf-chip {{
    display:inline-flex; align-items:center; gap:6px; padding:6px 12px; border-radius:999px;
    background:#121821; border:1px solid #1F2937; color:#D1D5DB; margin-right:8px; margin-bottom:8px;
}}
.hf-chip.active {{ background:#0C2A21; border-color:{PRIMARY}; color:#CFFAEA; }}

/* Card */
.hf-card {{
    background:#0F1418; border:1px solid #1F2937; border-radius:16px; padding:18px; margin-bottom:14px;
}}
.badge {{
    display:inline-block; padding:6px 10px; border-radius:999px; font-size:12px; border:1px solid #1F2937;
}}
.badge-green {{ background:#0C2A21; color:#A7F3D0; border-color:{PRIMARY}; }}
.source-btn {{
    display:inline-flex; align-items:center; gap:8px; padding:8px 12px; border-radius:12px; border:1px solid #1F2937;
    color:#D1D5DB; text-decoration:none; margin-right:8px; margin-top:6px; background:#10161D;
}}
.right-card {{
    background:#0F1418; border:1px solid #1F2937; border-radius:16px; padding:16px; margin-bottom:14px;
}}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ------------------------------
# Session State for filters
# ------------------------------
if "active_category" not in st.session_state:
    st.session_state.active_category = "All"
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "claims" not in st.session_state:
    st.session_state.claims = []

categories = ["All", "Nutrition", "Exercise", "Mental Health", "Wellness"]

def render_header() -> None:
    col1, col2, col3 = st.columns([3, 6, 3])
    with col1:
        st.markdown(
            """
            <div class="hf-header">
              <div class="hf-brand">
                <div class="hf-logo">🧠</div>
                <div>HealthFact AI</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        nav_cols = st.columns([1,1,1,1,1])
        with nav_cols[0]:
            if st.button("Home", key="nav-home"):
                st.session_state.page = "Home"
        with nav_cols[1]:
            if st.button("Categories", key="nav-categories"):
                st.session_state.page = "Categories"
        with nav_cols[2]:
            if st.button("Quiz", key="nav-quiz"):
                st.session_state.page = "Quiz"
                st.session_state["start_quiz"] = True
        with nav_cols[3]:
            if st.button("My Progress", key="nav-progress"):
                st.session_state.page = "My Progress"
        with nav_cols[4]:
            if st.button("Admin", key="nav-admin"):
                st.session_state.page = "Admin"
    with col3:
        st.markdown(
            """
            <div class="hf-header">
              <div class="hf-actions">
                <span class="btn">Login</span>
                <span class="btn btn-primary">Sign Up</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_search() -> str:
    query = st.text_input("", placeholder="Search health facts, topics, or ask a question...", label_visibility="collapsed")
    chip_cols = st.columns(len(categories))
    for idx, name in enumerate(categories):
        with chip_cols[idx]:
            if st.button(name, key=f"chip-{name}"):
                st.session_state.active_category = name
    return query


def render_fact_card(fact: Dict) -> None:
    st.markdown(
        f"""
        <div class="hf-card">
          <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
            <span class="badge">{fact.get('category', 'Nutrition')}</span>
            <span class="badge badge-green">{fact.get('confidence', '92%')} Confidence</span>
          </div>
          <div style="font-size:22px; font-weight:700; margin-bottom:8px;">{fact['title']}</div>
          <div style="color:#9CA3AF; line-height:1.6;">{fact['summary']}</div>
          <div style="margin-top:12px;">
            {''.join([f"<a class='source-btn' href='{s['url']}' target='_blank'>{s['name']}</a>" for s in fact['sources']])}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def right_sidebar() -> None:
    st.markdown(
        """
        <div class="right-card">
          <div style="display:flex; align-items:center; gap:12px;">
            <div style="width:56px; height:56px; border-radius:16px; background:#111827; border:1px solid #1F2937;
                        display:flex; align-items:center; justify-content:center; font-size:24px;">👤</div>
            <div>
              <div style="font-weight:700;">Alex Johnson</div>
              <div style="color:#9CA3AF; font-size:13px;">156 facts learned</div>
            </div>
          </div>
        </div>

        <div class="right-card">
          <div style="font-weight:700; margin-bottom:8px;">Daily Streak</div>
          <div style="display:flex; gap:8px;">
            <div class="badge" style="background:#111827;">3</div>
            <div class="badge" style="background:#111827;">5</div>
            <div class="badge" style="background:#111827;">2</div>
            <div class="badge" style="background:#111827;">7</div>
            <div class="badge" style="background:#111827;">4</div>
            <div class="badge" style="background:#111827;">6</div>
            <div class="badge" style="background:#111827;">3</div>
          </div>
          <div style="color:#9CA3AF; font-size:12px; margin-top:8px;">Facts learned this week</div>
        </div>

        <div class="right-card">
          <div style="font-weight:700; margin-bottom:8px;">Achievements</div>
          <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:12px;">
            <div class="hf-card" style="padding:14px; text-align:center;">🏅<div style="margin-top:6px;">Fact Explorer</div></div>
            <div class="hf-card" style="padding:14px; text-align:center;">🥇<div style="margin-top:6px;">Health Guru</div></div>
            <div class="hf-card" style="padding:14px; text-align:center;">🎯<div style="margin-top:6px;">Quiz Master</div></div>
            <div class="hf-card" style="padding:14px; text-align:center;">🔥<div style="margin-top:6px;">Streak</div></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Daily Quiz card
    st.markdown(
        """
        <div class="right-card" style="background: radial-gradient(120% 120% at 0% 0%, #0F1418 0%, #0D1216 60%, #0B0F12 100%);">
          <div style="font-weight:700; display:flex; align-items:center; gap:8px; margin-bottom:6px;">
            <span>🎯</span>
            <span>Daily Quiz</span>
          </div>
          <div style="color:#9CA3AF; margin-bottom:10px;">Test your knowledge with today's health quiz!</div>
        """,
        unsafe_allow_html=True,
    )
    start = st.button("Start Quiz", key="daily_quiz_btn")
    st.markdown(
        """
        <div style="color:#9CA3AF; font-size:13px; text-align:center; margin-top:6px;">Complete daily quizzes to earn bonus points</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if start:
        st.session_state["start_quiz"] = True


def fetch_featured_fact(query: str) -> Dict:
    # Placeholder using backend hook if available
    try:
        if query:
            _ = requests.get(f"{API_URL}/search", params={"q": query}, timeout=2)
    except Exception:
        pass
    return {
        "category": "Nutrition",
        "confidence": "92%",
        "title": "The Power of Mediterranean Diet on Brain Health",
        "summary": (
            "Research shows that following a Mediterranean diet rich in olive oil, fish, nuts, "
            "and vegetables can reduce the risk of cognitive decline by up to 35%. The omega-3 "
            "fatty acids and antioxidants in these foods help protect brain cells and improve memory function."
        ),
        "sources": [
            {"name": "Harvard Health", "url": "https://www.health.harvard.edu/"},
            {"name": "Mayo Clinic", "url": "https://www.mayoclinic.org/"},
            {"name": "Nature Medicine", "url": "https://www.nature.com/nm/"},
        ],
    }


def legacy_tools() -> None:
    with st.expander("Check a Health Claim"):
        claim = st.text_area("Enter a health claim:")
        if st.button("Check Claim") and claim.strip():
            try:
                response = requests.post(f"{API_URL}/check_claim", json={"claim": claim}, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"Result: {data['result']}")
                    st.write(f"Explanation: {data['explanation']}")
                    st.markdown(f"[Trusted Source]({data['source']})")
                else:
                    st.error("Error connecting to backend.")
            except Exception as ex:
                st.error(f"Backend not available: {ex}")

    with st.expander("Quiz Mode", expanded=st.session_state.get("start_quiz", False)):
        start_clicked = st.button("Start Quiz") or st.session_state.get("start_quiz", False)
        if start_clicked:
            try:
                response = requests.get(f"{API_URL}/quiz", timeout=10)
                if response.status_code == 200:
                    questions = response.json().get("questions", [])
                    for q in questions:
                        st.write(q.get("question", ""))
                        answer = st.radio("Your answer:", q.get("options", []), key=q.get("id", "q"))
                        if st.button(f"Submit {q.get('id', '')}"):
                            st.write("✅ Correct!" if answer == q.get("answer") else "❌ Wrong")
                else:
                    st.error("Could not fetch quiz questions.")
            except Exception as ex:
                st.error(f"Backend not available: {ex}")
        # Reset flag after rendering so it doesn't loop
        if st.session_state.get("start_quiz"):
            st.session_state["start_quiz"] = False


# ------------------------------
# Render
# ------------------------------
render_header()

if st.session_state.page == "Home":
    query = render_search()
    left, right = st.columns([2.5, 1])
    with left:
        fact = fetch_featured_fact(query)
        render_fact_card(fact)
    with right:
        right_sidebar()
    legacy_tools()
elif st.session_state.page == "Categories":
    st.subheader("Browse Categories")
    _ = render_search()
    st.info(f"Active category: {st.session_state.active_category}")
elif st.session_state.page == "Quiz":
    legacy_tools()
elif st.session_state.page == "My Progress":
    st.subheader("My Progress")
    try:
        import pandas as pd
        import plotly.express as px
        # Demo dataset
        progress_data = pd.DataFrame({
            "day": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
            "facts": [3,5,2,7,4,6,3],
        })
        fig = px.bar(progress_data, x="day", y="facts", title="Facts Learned This Week",
                     color_discrete_sequence=[PRIMARY])
        st.plotly_chart(fig, use_container_width=True)

        categories_data = pd.DataFrame({
            "category": ["Nutrition","Exercise","Mental Health","Wellness"],
            "count": [24,18,32,12],
        })
        pie = px.pie(categories_data, names="category", values="count", title="Learned by Category")
        st.plotly_chart(pie, use_container_width=True)
    except Exception as ex:
        st.info("Charts unavailable. Install pandas and plotly to enable graphs.")

    st.metric("Total Facts Learned", 156)
    st.metric("Current Streak", "12 days")
elif st.session_state.page == "Admin":
    st.subheader("Admin Panel")
    st.caption("Add new misinformation claims or update explanations and trusted links.")

    st.write("Add Claim")
    with st.form("add_claim_form", clear_on_submit=True):
        c_text = st.text_area("Claim text")
        c_truth = st.selectbox("Verdict", ["True","False","Misleading","Unverified"])
        c_expl = st.text_area("Explanation")
        c_source = st.text_input("Trusted source URL")
        submitted = st.form_submit_button("Add")
        if submitted and c_text.strip():
            st.session_state.claims.append({
                "claim": c_text, "verdict": c_truth, "explanation": c_expl, "source": c_source,
            })
            try:
                requests.post(f"{API_URL}/claims", json=st.session_state.claims[-1], timeout=3)
            except Exception:
                pass
            st.success("Claim added")

    st.write("Update Existing")
    if st.session_state.claims:
        options = [c["claim"][:60] + ("…" if len(c["claim"])>60 else "") for c in st.session_state.claims]
        idx = st.selectbox("Choose claim", list(range(len(options))), format_func=lambda i: options[i])
        selected = st.session_state.claims[idx]
        new_expl = st.text_area("Explanation", value=selected.get("explanation",""), key="upd_expl")
        new_src = st.text_input("Trusted source URL", value=selected.get("source",""), key="upd_src")
        if st.button("Update"):
            selected["explanation"] = new_expl
            selected["source"] = new_src
            try:
                requests.put(f"{API_URL}/claims/{idx}", json=selected, timeout=3)
            except Exception:
                pass
            st.success("Updated")
