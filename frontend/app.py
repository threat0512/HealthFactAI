import streamlit as st
import requests
from typing import List, Dict

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="HealthFact AI", page_icon="🧠", layout="wide")

# ------------------------------
# Theme & CSS helpers
# ------------------------------
PRIMARY = "#6366F1"  # indigo-500
ACCENT = "#10B981"   # emerald-500
SECONDARY = "#8B5CF6"  # violet-500

# Theme switching
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def get_theme_colors():
    if st.session_state.theme == "dark":
        return {
            "bg": "#0F172A",  # slate-900
            "card_bg": "#1E293B",  # slate-800
            "border": "#334155",  # slate-600
            "text": "#F1F5F9",  # slate-100
            "text_secondary": "#94A3B8",  # slate-400
            "accent": "#6366F1",  # indigo-500
            "secondary": "#8B5CF6",  # violet-500
            "success": "#10B981",  # emerald-500
            "warning": "#F59E0B",  # amber-500
            "error": "#EF4444",  # red-500
        }
    else:
        return {
            "bg": "#FFFFFF",  # white
            "card_bg": "#F8FAFC",  # slate-50
            "border": "#E2E8F0",  # slate-200
            "text": "#0F172A",  # slate-900
            "text_secondary": "#64748B",  # slate-500
            "accent": "#6366F1",  # indigo-500
            "secondary": "#8B5CF6",  # violet-500
            "success": "#10B981",  # emerald-500
            "warning": "#F59E0B",  # amber-500
            "error": "#EF4444",  # red-500
        }

def generate_css():
    colors = get_theme_colors()
    return f"""
<style>
/* Base theme */
.stApp {{
    background: {colors['bg']};
    color: {colors['text']};
}}

/* Streamlit buttons styling */
.stButton > button {{
    background: {colors['card_bg']} !important;
    border: 2px solid {colors['border']} !important;
    color: {colors['text']} !important;
    border-radius: 12px !important;
    height: 44px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}}
.stButton > button:hover {{
    border-color: {colors['accent']} !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2) !important;
}}
.stButton > button:active {{
    background: {colors['accent']} !important;
    border-color: {colors['accent']} !important;
    color: white !important;
}}

/* Header bar */
.hf-header {{
    display: flex; align-items: center; justify-content: space-between;
    background: {colors['card_bg']}; border: 1px solid {colors['border']}; border-radius: 16px;
    padding: 16px 20px; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}}
.hf-brand {{ display:flex; align-items:center; gap:16px; font-weight:800; font-size:20px; }}
.hf-logo {{
    width: 44px; height: 44px; border-radius: 12px; background: linear-gradient(135deg, {colors['accent']}, {colors['secondary']});
    display:flex; align-items:center; justify-content:center; border:2px solid {colors['border']};
    color: white; font-size: 20px;
}}

/* Navigation buttons */
.nav-btn {{
    background: {colors['card_bg']} !important;
    border: 2px solid {colors['border']} !important;
    color: {colors['text']} !important;
    border-radius: 12px !important;
    height: 44px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}}
.nav-btn:hover {{
    border-color: {colors['accent']} !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2) !important;
}}
.nav-btn.active {{
    background: {colors['accent']} !important;
    border-color: {colors['accent']} !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
}}

/* Search bar */
.stTextInput>div>div>input {{
    height: 52px; border-radius: 16px; border: 2px solid {colors['border']}; padding: 12px 20px;
    background: {colors['card_bg']}; color: {colors['text']}; font-size: 16px;
    transition: all 0.2s ease;
}}
.stTextInput>div>div>input:focus {{
    border-color: {colors['accent']}; box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}}

/* Category chips */
.category-chip {{
    background: {colors['card_bg']} !important;
    border: 2px solid {colors['border']} !important;
    color: {colors['text']} !important;
    border-radius: 999px !important;
    padding: 8px 16px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}}
.category-chip:hover {{
    border-color: {colors['accent']} !important;
    transform: translateY(-1px) !important;
}}
.category-chip.active {{
    background: {colors['accent']} !important;
    border-color: {colors['accent']} !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
}}

/* Cards */
.hf-card {{
    background: {colors['card_bg']}; border: 1px solid {colors['border']}; border-radius: 20px; 
    padding: 24px; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    transition: all 0.2s ease;
}}
.hf-card:hover {{
    transform: translateY(-2px); box-shadow: 0 8px 25px -5px rgba(0, 0, 0, 0.1);
}}

.badge {{
    display: inline-block; padding: 8px 16px; border-radius: 999px; font-size: 12px; 
    border: 1px solid {colors['border']}; color: {colors['text_secondary']}; font-weight: 600;
}}
.badge-category {{ 
    background: rgba(99, 102, 241, 0.1); color: {colors['accent']}; border-color: {colors['accent']};
}}
.badge-confidence {{ 
    background: rgba(16, 185, 129, 0.1); color: {colors['success']}; border-color: {colors['success']};
}}

.source-btn {{
    display: inline-flex; align-items: center; gap: 8px; padding: 10px 16px; border-radius: 12px; 
    border: 1px solid {colors['border']}; color: {colors['text']}; text-decoration: none; 
    margin-right: 12px; margin-top: 8px; background: {colors['card_bg']}; font-weight: 500;
    transition: all 0.2s ease;
}}
.source-btn:hover {{
    border-color: {colors['accent']}; transform: translateY(-1px);
}}

.right-card {{
    background: {colors['card_bg']}; border: 1px solid {colors['border']}; border-radius: 20px; 
    padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}}

/* Theme toggle button */
.theme-toggle {{
    position: fixed; top: 20px; right: 20px; z-index: 1000;
    background: {colors['accent']}; color: white; border: none; border-radius: 50px;
    padding: 12px 20px; font-weight: 600; cursor: pointer; box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    transition: all 0.2s ease;
}}
.theme-toggle:hover {{
    transform: translateY(-1px); box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
}}

/* Progress bar */
.progress-bar {{
    height: 8px; width: 100%; background: {colors['border']}; border-radius: 999px; margin-top: 12px;
}}
.progress-fill {{
    height: 8px; width: 60%; background: linear-gradient(90deg, {colors['accent']}, {colors['secondary']}); 
    border-radius: 999px; transition: width 0.3s ease;
}}

/* Metrics */
.stMetric {{
    background: {colors['card_bg']}; border: 1px solid {colors['border']}; border-radius: 16px; 
    padding: 20px; margin: 10px 0;
}}
</style>
"""

# Apply CSS dynamically
st.markdown(generate_css(), unsafe_allow_html=True)

# ------------------------------
# Session State for filters
# ------------------------------
if "active_category" not in st.session_state:
    st.session_state.active_category = "All"
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "claims" not in st.session_state:
    st.session_state.claims = []
if "user" not in st.session_state:
    st.session_state.user = {"name": "John Doe", "role": "Health Enthusiast"}

categories = ["All", "Nutrition", "Exercise", "Mental Health", "Wellness"]

def render_header() -> None:
    # Theme toggle button in the top right
    col1, col2, col3 = st.columns([6, 1, 1])
    with col3:
        if st.button(f"{'🌙' if st.session_state.theme == 'light' else '☀️'}", 
                     help=f"Switch to {'dark' if st.session_state.theme == 'light' else 'light'} mode"):
            st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
            st.rerun()
    
    # Header with logo and brand
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
    
    # Navigation buttons in a single row
    nav_cols = st.columns(5, gap="small")
    with nav_cols[0]:
        is_active = st.session_state.page == "Home" or (st.session_state.page == "Landing" and not st.session_state.user)
        if st.button("Home", key="nav-home", use_container_width=True, 
                    help="Go to Home page"):
            st.session_state.page = "Home" if st.session_state.user else "Landing"
    with nav_cols[1]:
        is_active = st.session_state.page == "Categories"
        if st.button("Categories", key="nav-categories", use_container_width=True,
                    help="Browse health categories"):
            st.session_state.page = "Categories"
    with nav_cols[2]:
        is_active = st.session_state.page == "Quiz"
        if st.button("Quiz", key="nav-quiz", use_container_width=True,
                    help="Take health quizzes"):
            if st.session_state.user:
                st.session_state.page = "Quiz"
                st.session_state["start_quiz"] = True
            else:
                st.session_state.page = "Auth"
    with nav_cols[3]:
        is_active = st.session_state.page == "Progress"
        if st.button("Progress", key="nav-progress", use_container_width=True,
                    help="View your progress"):
            st.session_state.page = "Progress"
    with nav_cols[4]:
        is_active = st.session_state.page == "Admin"
        if st.button("Admin", key="nav-admin", use_container_width=True,
                    help="Admin panel"):
            st.session_state.page = "Admin" if st.session_state.user else "Auth"
    
    # User actions on the right
    if st.session_state.user:
        if st.button("Logout", help="Sign out"):
            st.session_state.user = None
            st.session_state.page = "Landing"
    else:
        # Empty space for now
        st.write("")
    



def render_search() -> str:
    query = st.text_input("", placeholder="Ask about nutrition, exercise, mental health...", label_visibility="collapsed")
    
    # Category chips with better styling
    st.markdown("<div style='margin: 20px 0;'>", unsafe_allow_html=True)
    chip_cols = st.columns(len(categories), gap="small")
    for idx, name in enumerate(categories):
        with chip_cols[idx]:
            is_active = st.session_state.active_category == name
            if st.button(name, key=f"chip-{name}", 
                        help=f"Filter by {name} category"):
                st.session_state.active_category = name
    st.markdown("</div>", unsafe_allow_html=True)
    
    return query


def render_landing() -> None:
    colors = get_theme_colors()
    st.markdown(
        f"""
        <div style="text-align: center; margin: 60px 0 40px 0;">
          <div style="font-size: 48px; font-weight: 800; margin-bottom: 16px; color: {colors['text']};">
            Fight Health Misinformation
          </div>
          <div style="color: {colors['text_secondary']}; font-size: 20px; line-height: 1.6;">
            AI-powered fact-checking • Interactive learning • Trusted sources
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Features
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown(
            f"""
            <div class="hf-card">
              <div style="font-size: 20px; font-weight: 700; margin-bottom: 12px; color: {colors['text']};">Bust Health Myths</div>
              <div style="color: {colors['text_secondary']}; margin-bottom: 16px;">Separate fact from fiction with AI-powered analysis</div>
              <div style="display: flex; gap: 8px;">
                <span style="background: {colors['accent']}; color: white; padding: 6px 12px; border-radius: 999px; font-size: 12px;">Quiz</span>
                <span style="background: {colors['success']}; color: white; padding: 6px 12px; border-radius: 999px; font-size: 12px;">Learn</span>
                <span style="background: {colors['secondary']}; color: white; padding: 6px 12px; border-radius: 999px; font-size: 12px;">Track</span>
              </div>
            </div>
            <div class="hf-card">
              <div style="font-size: 20px; font-weight: 700; margin-bottom: 12px; color: {colors['text']};">Interactive Learning</div>
              <div style="color: {colors['text_secondary']}; margin-bottom: 16px;">Gamified fact-checking</div>
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
              <div style="font-size: 20px; font-weight: 700; margin-bottom: 12px; color: {colors['text']};">Build Media Literacy</div>
              <div style="color: {colors['text_secondary']}; margin-bottom: 16px;">Learn to identify reliable health information sources</div>
              <div style="background: {colors['success']}; color: white; padding: 6px 12px; border-radius: 999px; font-size: 12px; display: inline-block;">
                Progress: 70%
              </div>
            </div>
            <div class="hf-card">
              <div style="font-size: 20px; font-weight: 700; margin-bottom: 12px; color: {colors['text']};">Accessible Everywhere</div>
              <div style="color: {colors['text_secondary']}; margin-bottom: 16px;">Multiple languages • Global health literacy</div>
              <div style="display: flex; gap: 8px;">
                <span style="background: {colors['accent']}; color: white; padding: 6px 12px; border-radius: 999px; font-size: 12px;">EN</span>
                <span style="background: {colors['secondary']}; color: white; padding: 6px 12px; border-radius: 999px; font-size: 12px;">ES</span>
                <span style="background: {colors['warning']}; color: white; padding: 6px 12px; border-radius: 999px; font-size: 12px;">🌐</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Centered CTA
    st.markdown(
        f"""
        <div style="text-align: center; margin: 40px 0;">
          <button onclick="window.parent.postMessage({{type: 'start-fact-checking'}}, '*')" 
                  style="background: {colors['accent']}; color: white; border: none; border-radius: 16px; 
                         padding: 16px 32px; font-size: 18px; font-weight: 600; cursor: pointer;
                         box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3); transition: all 0.2s ease;">
            Start Fact-Checking
          </button>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Handle the button click
    if st.button("Start Fact-Checking", key="landing-cta", use_container_width=True):
        st.session_state.page = "Auth"


def render_auth() -> None:
    colors = get_theme_colors()
    st.markdown(f"""
    <div style="text-align: center; margin: 40px 0;">
        <div style="font-size: 32px; font-weight: 800; color: {colors['text']}; margin-bottom: 8px;">Welcome Back</div>
        <div style="color: {colors['text_secondary']}; font-size: 18px;">Sign in to continue your health journey</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Center the form
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("auth_form"):
            st.markdown(f"""
            <div style="background: {colors['card_bg']}; border: 1px solid {colors['border']}; border-radius: 20px; padding: 32px; margin: 20px 0;">
                <div style="font-size: 24px; font-weight: 700; margin-bottom: 24px; color: {colors['text']}; text-align: center;">Sign In</div>
            """, unsafe_allow_html=True)
            
            email = st.text_input("Email", placeholder="Enter your email address")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            st.markdown(f"""
            <div style="margin-top: 24px;">
            """, unsafe_allow_html=True)
            
            ok = st.form_submit_button("Continue", type="primary", use_container_width=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
            
            if ok:
                st.session_state.user = {"email": email}
                st.session_state.page = "Home"

def render_fact_card(fact: Dict) -> None:
    colors = get_theme_colors()
    st.markdown(
        f"""
        <div class="hf-card">
          <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:16px;">
            <div style="display:flex; align-items:center; gap:12px;">
              <span class="badge badge-category">{fact.get('category', 'Nutrition')}</span>
            </div>
            <span class="badge badge-confidence">{fact.get('confidence', '92%')} confidence</span>
          </div>
          <div style="font-size:24px; font-weight:800; margin-bottom:12px; color:{colors['text']};">{fact['title']}</div>
          <div style="color:{colors['text_secondary']}; line-height:1.7; font-size:16px;">{fact['summary']}</div>
          <div style="margin-top:20px;">
            {''.join([f"<a class='source-btn' href='{s['url']}' target='_blank'>{s['name']}</a>" for s in fact['sources']])}
          </div>
          <div style="display:flex; justify-content:flex-end; color:{colors['text_secondary']}; margin-top:12px; font-size:14px;">
            🔗 Share • 📖 Read More
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def right_sidebar() -> None:
    colors = get_theme_colors()
    st.markdown(
        f"""
        <div class="right-card">
          <div style="display:flex; align-items:center; gap:16px;">
            <div style="width:64px; height:64px; border-radius:999px; background:linear-gradient(135deg, {colors['accent']}, {colors['secondary']}); 
                        display:flex; align-items:center; justify-content:center; font-size:28px; color:white;">🙂</div>
            <div>
              <div style="font-weight:700; font-size:18px; color:{colors['text']};">John Doe</div>
              <div style="color:{colors['text_secondary']}; font-size:14px;">Health Enthusiast</div>
            </div>
          </div>
        </div>

        <div class="right-card">
          <div style="font-weight:700; margin-bottom:12px; color:{colors['text']};">Daily Streak</div>
          <div style="display:flex; align-items:center; justify-content:space-between;">
            <div style="color:{colors['text_secondary']}; font-size:16px;">🔥 12 days</div>
          </div>
          <div class="progress-bar">
            <div class="progress-fill"></div>
          </div>
        </div>

        <div class="right-card">
          <div style="font-weight:700; margin-bottom:12px; color:{colors['text']};">Achievements</div>
          <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:12px;">
            <div class="hf-card" style="padding:16px; text-align:center; background:{colors['card_bg']}; border:1px solid {colors['border']};">
              🎓<div style="margin-top:8px; font-size:12px; color:{colors['text_secondary']};">Learner</div>
            </div>
            <div class="hf-card" style="padding:16px; text-align:center; background:{colors['card_bg']}; border:1px solid {colors['border']};">
              🔥<div style="margin-top:8px; font-size:12px; color:{colors['text_secondary']};">Streak</div>
            </div>
            <div class="hf-card" style="padding:16px; text-align:center; background:{colors['card_bg']}; border:1px solid {colors['border']};">
              🏆<div style="margin-top:8px; font-size:12px; color:{colors['text_secondary']};">Expert</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Daily Quiz card
    st.markdown(
        f"""
        <div class="right-card">
          <div style="font-weight:700; display:flex; align-items:center; gap:8px; margin-bottom:8px; color:{colors['text']};">
            <span>📌</span>
            <span>Daily Quiz Challenge</span>
          </div>
          <div style="color:{colors['text_secondary']}; margin-bottom:16px; font-size:14px;">
            Test your knowledge with today's health quiz!
          </div>
        """,
        unsafe_allow_html=True,
    )
    start = st.button("Start Quiz", key="daily_quiz_btn", help="Begin today's quiz challenge")
    st.markdown(
        """
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
    # Health Claim Checker
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

    # Quiz Mode
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

            # Reset quiz flag after rendering
            if st.session_state.get("start_quiz"):
                st.session_state["start_quiz"] = False



# ------------------------------
# Render
# ------------------------------
render_header()

if st.session_state.page == "Landing":
    render_landing()
elif st.session_state.page == "Auth":
    render_auth()
elif st.session_state.page == "Home":
    query = render_search()
    left, right = st.columns([2.5, 1])
    with left:
        fact = fetch_featured_fact(query)
        render_fact_card(fact)
    with right:
        right_sidebar()
    # Remove legacy tools for cleaner UI
elif st.session_state.page == "Categories":
    colors = get_theme_colors()
    st.subheader("Browse Categories")
    _ = render_search()
    
    # Better styled active category indicator
    st.markdown(f"""
    <div style="background: {colors['accent']}; color: white; padding: 16px; border-radius: 16px; text-align: center; margin: 20px 0;">
        <div style="font-weight: 700; font-size: 18px;">Active Category</div>
        <div style="font-size: 24px; margin-top: 8px;">{st.session_state.active_category}</div>
    </div>
    """, unsafe_allow_html=True)
elif st.session_state.page == "Quiz":
    legacy_tools()
elif st.session_state.page == "Progress":
    colors = get_theme_colors()
    st.subheader("Progress")
    try:
        import pandas as pd
        import plotly.express as px
        
        # Demo dataset
        progress_data = pd.DataFrame({
            "day": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
            "facts": [3,5,2,7,4,6,3],
        })
        
        # Create a better-looking chart with theme colors
        fig = px.bar(progress_data, x="day", y="facts", 
                     title="Facts Learned This Week",
                     color_discrete_sequence=[colors['accent']])
        fig.update_layout(
            plot_bgcolor=colors['card_bg'],
            paper_bgcolor=colors['card_bg'],
            font=dict(color=colors['text']),
            title_font_color=colors['text']
        )
        fig.update_xaxes(gridcolor=colors['border'], zerolinecolor=colors['border'])
        fig.update_yaxes(gridcolor=colors['border'], zerolinecolor=colors['border'])
        st.plotly_chart(fig, use_container_width=True)

        categories_data = pd.DataFrame({
            "category": ["Nutrition","Exercise","Mental Health","Wellness"],
            "count": [24,18,32,12],
        })
        pie = px.pie(categories_data, names="category", values="count", 
                     title="Learned by Category",
                     color_discrete_sequence=[colors['accent'], colors['secondary'], colors['success'], colors['warning']])
        pie.update_layout(
            plot_bgcolor=colors['card_bg'],
            paper_bgcolor=colors['card_bg'],
            font=dict(color=colors['text']),
            title_font_color=colors['text']
        )
        st.plotly_chart(pie, use_container_width=True)
    except Exception as ex:
        st.info("Charts unavailable. Install pandas and plotly to enable graphs.")

    # Better styled metrics
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stMetric">
            <div style="font-size: 24px; font-weight: 700; color: {colors['text']};">156</div>
            <div style="color: {colors['text_secondary']};">Total Facts Learned</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stMetric">
            <div style="font-size: 24px; font-weight: 700; color: {colors['text']};">12 days</div>
            <div style="color: {colors['text_secondary']};">Current Streak</div>
        </div>
        """, unsafe_allow_html=True)
elif st.session_state.page == "Admin":
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
            st.session_state.claims.append({
                "claim": c_text, "verdict": c_truth, "explanation": c_expl, "source": c_source,
            })
            try:
                requests.post(f"{API_URL}/claims", json=st.session_state.claims[-1], timeout=3)
            except Exception:
                pass
            st.success("✅ Claim added successfully!")

    st.markdown("</div>", unsafe_allow_html=True)

    # Update Existing section
    if st.session_state.claims:
        st.markdown(f"""
        <div class="hf-card">
            <div style="font-weight: 700; font-size: 18px; margin-bottom: 16px; color: {colors['text']};">Update Existing Claims</div>
        """, unsafe_allow_html=True)
        
        options = [c["claim"][:60] + ("…" if len(c["claim"])>60 else "") for c in st.session_state.claims]
        idx = st.selectbox("Choose claim to update", list(range(len(options))), format_func=lambda i: options[i])
        selected = st.session_state.claims[idx]
        
        new_expl = st.text_area("Explanation", value=selected.get("explanation",""), key="upd_expl")
        new_src = st.text_input("Trusted source URL", value=selected.get("source",""), key="upd_src")
        
        if st.button("Update Claim", type="primary"):
            selected["explanation"] = new_expl
            selected["source"] = new_src
            try:
                requests.put(f"{API_URL}/claims/{idx}", json=selected, timeout=3)
            except Exception:
                pass
            st.success("✅ Claim updated successfully!")
        
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No claims available to update. Add some claims first!")
