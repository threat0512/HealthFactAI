import streamlit as st
from styles.theme import get_theme_colors
from utils.state import set_page, is_authenticated


def render_landing() -> None:
    """Render the landing page for unauthenticated users"""
    colors = get_theme_colors()

    # If user is authenticated, redirect to dashboard
    if is_authenticated():
        set_page("Home")
        st.rerun()
        return

    # HERO
    st.markdown(
        f"""
        <div style="text-align:center; margin: 12px 0 20px 0;">
          <h1 style="margin:0; font-size:40px; font-weight:800; color: {colors['text']};">Empowering youth to fight health misinformation</h1>
          <div style="font-size:18px; font-weight:700; color: {colors['accent']}; margin-top:8px;">Through Media &amp; Information Literacy</div>
          <p style="color: {colors['text_secondary']}; font-size:15px; line-height:1.6; max-width:1000px; margin:14px auto;">HealthFactAI — check the claim, trust the science. Learn how to spot false health advice, verify sources, and build resilience online.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # PROBLEM (full width)
    st.markdown(
        f"""
        <div class="hf-card" style="margin-bottom:18px; padding:18px;">
          <div style="font-size:18px; font-weight:700; color: {colors['text']}; margin-bottom:8px;">Problem: Health misinformation is everywhere</div>
          <ul style="color: {colors['text_secondary']}; line-height:1.6; margin-left:18px;">
            <li><strong>Health misinformation spreads three times faster than accurate information (WHO).</strong></li>
            <li>Examples of false claims:
              <ul style="margin-top:6px;">
                <li>"Garlic soup proven to cure COVID overnight!"</li>
                <li>"Drink 2 liters of cola daily — doctor says it burns fat instantly!"</li>
                <li>"Bananas are 10x stronger than antibiotics, say experts on WhatsApp"</li>
              </ul>
            </li>
            <li>Youth are among the most exposed and vulnerable online.</li>
            <li><strong>Consequences:</strong> health risks, panic, confusion, and loss of trust in science.</li>
          </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Quadrant grid: 2x2 equal boxes (What we do | Get involved) / (Tip | Target audience)
    # Each box uses the same hf-card styles and a fixed min-height to appear equal.
    row1c1, row1c2 = st.columns([1, 1], gap="large")
    row2c1, row2c2 = st.columns([1, 1], gap="large")

    box_style = f"padding:18px; min-height:180px; display:flex; flex-direction:column; justify-content:space-between;"

    with row1c1:
        st.markdown(
            f"""
            <div class="hf-card" style="{box_style}">
              <div>
                <div style="font-size:20px; font-weight:700; color: {colors['text']}; margin-bottom:8px;">What we do</div>
                <div style="color: {colors['text_secondary']}; margin-bottom:12px;">HealthFactAI helps youth evaluate health claims, learn critical skills, and practice with quizzes.</div>
              </div>
              <div style="display:flex; gap:8px; align-items:center;">
                <span style="background:{colors['accent']}; color:white; padding:6px 12px; border-radius:999px; font-size:12px;">Check claims</span>
                <span style="background:{colors['success']}; color:white; padding:6px 12px; border-radius:999px; font-size:12px;">Trusted sources</span>
                <span style="background:{colors['secondary']}; color:white; padding:6px 12px; border-radius:999px; font-size:12px;">Quizzes</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with row1c2:
        st.markdown(
            f"""
            <div class="hf-card" style="{box_style}">
              <div>
                <div style="display:flex; align-items:center; gap:12px; margin-bottom:8px;">
                  <div style="width:44px; height:44px; border-radius:8px; background:{colors['card_bg']}; display:flex; align-items:center; justify-content:center;">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M3 11V5a1 1 0 0 1 1-1h3l7-3v12l-7-3H4a1 1 0 0 1-1-1z" fill="{colors['accent']}" />
                      <path d="M20 8v8a1 1 0 0 1-1 1h-2a3 3 0 0 0 0-6h2a1 1 0 0 1 1 1z" fill="{colors['secondary']}" />
                    </svg>
                  </div>
                  <div style="font-size:18px; font-weight:700; color: {colors['text']};">Get involved</div>
                </div>
                <div style="color: {colors['text_secondary']}; margin-bottom:12px;">Join workshops, share resources, and help spread accurate health information in your community. Help lead local sessions or bring classmates — we provide starter materials and facilitator guides for in-person or online formats.</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with row2c1:
        st.markdown(
            f"""
            <div class="hf-card" style="{box_style}">
              <div>
                <div style="font-size:18px; font-weight:700; color: {colors['text']}; margin-bottom:8px;">Tip</div>
                <div style="color: {colors['text_secondary']};">Always check whether a claim links to WHO, CDC, or peer-reviewed sources before sharing. If no clear source is provided, look for the author, publication date, and multiple independent confirmations. Use the AI fact checker for a quick scan, try a short quiz to practice, and report harmful claims to platform moderators when appropriate.</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with row2c2:
        st.markdown(
            f"""
            <div class="hf-card" style="{box_style}">
              <div style="text-align:center; width:100%;">
                <div style="font-size:18px; font-weight:700; color: {colors['text']}; margin-bottom:8px;">Target audience</div>
                <div style="color: {colors['text_secondary']};">Students and young people primarily, with a model that can be replicated across age groups and institutions.</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Impact header
    st.markdown(
        f"""
        <div class="hf-card" style="margin-top: 18px; padding:18px;">
          <div style="font-size:20px; font-weight:800; color: {colors['text']}; margin-bottom:10px;">Impact — Youth leading with clarity</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Quick stats row (four badges) — balanced, small cards to fill space
    s1, s2, s3, s4 = st.columns([1, 1, 1, 1], gap="large")
    stat_style = f"padding:12px; border-radius:10px; background:{colors['card_bg']}; text-align:center;"
    with s1:
        st.markdown(f"""<div style="{stat_style}"><div style="font-weight:800; font-size:20px; color:{colors['accent']};">1,500+</div><div style="color:{colors['text_secondary']}; font-size:13px;">Claims checked</div></div>""", unsafe_allow_html=True)
    with s2:
        st.markdown(f"""<div style="{stat_style}"><div style="font-weight:800; font-size:20px; color:{colors['success']};">200+</div><div style="color:{colors['text_secondary']}; font-size:13px;">Partner schools</div></div>""", unsafe_allow_html=True)
    with s3:
        st.markdown(f"""<div style="{stat_style}"><div style="font-weight:800; font-size:20px; color:{colors['warning']};">95%</div><div style="color:{colors['text_secondary']}; font-size:13px;">Accuracy in tests</div></div>""", unsafe_allow_html=True)
    with s4:
        st.markdown(f"""<div style="{stat_style}"><div style="font-weight:800; font-size:20px; color:{colors['secondary']};">20k</div><div style="color:{colors['text_secondary']}; font-size:13px;">Active learners</div></div>""", unsafe_allow_html=True)

    # Linear vertical Impact items
    impact_items = [
        ("Y", "Youth empowerment", "Equip young people with practical verification skills and confidence online.", colors['accent']),
        ("S", "Scalable approach", "Built to expand to classrooms, clubs, and community programmes.", colors['success']),
        ("R", "Real-world change", "Fewer scams, clearer health choices, and stronger public trust.", colors['warning']),
        ("B", "Better health decisions", "Encourages evidence-based choices and reduces harmful misinformation-driven actions.", colors['secondary']),
        ("M", "Measure progress", "Quizzes and simple dashboards track growth in media & information literacy.", colors['accent']),
    ]

    for letter, title, desc, bg in impact_items:
        lcol, rcol = st.columns([0.09, 0.91], gap="small")
        with lcol:
            st.markdown(f"""<div style="width:44px; height:44px; border-radius:8px; background:{bg}; display:flex; align-items:center; justify-content:center; color:white; font-weight:800;">{letter}</div>""", unsafe_allow_html=True)
        with rcol:
            st.markdown(f"""<div style="margin-bottom:10px;"><div style="font-weight:700; color: {colors['text']};">{title}</div><div style="color: {colors['text_secondary']};">{desc}</div></div>""", unsafe_allow_html=True)

    # How it works — three evenly spaced steps to fill the horizontal gap
    st.markdown("""
      <div style="margin-top:18px; margin-bottom:12px;">
        <div style="font-size:18px; font-weight:800; color: var(--hf-text);">How it works</div>
      </div>
    """, unsafe_allow_html=True)

    h1, h2, h3 = st.columns([1, 1, 1], gap="large")
    step_style = f"padding:16px; text-align:center; border-radius:12px; background:{colors['card_bg']}; min-height:120px; display:flex; flex-direction:column; justify-content:center;"
    with h1:
        st.markdown(f"""<div style="{step_style}"><div style="width:48px; height:48px; margin:0 auto 10px; border-radius:10px; background:linear-gradient(180deg,{colors['accent']},{colors['secondary']});"></div><div style="font-weight:700; color:{colors['text']};">Check a claim</div><div style="color:{colors['text_secondary']}; font-size:13px; margin-top:6px;">Paste a headline or claim and get a fast, evidence-based summary.</div></div>""", unsafe_allow_html=True)
    with h2:
        st.markdown(f"""<div style="{step_style}"><div style="width:48px; height:48px; margin:0 auto 10px; border-radius:50%; background:radial-gradient(circle at 40% 30%, {colors['accent']}, {colors['success']});"></div><div style="font-weight:700; color:{colors['text']};">Practice & learn</div><div style="color:{colors['text_secondary']}; font-size:13px; margin-top:6px;">Short quizzes and micro-lessons help build lasting skills.</div></div>""", unsafe_allow_html=True)
    with h3:
        st.markdown(f"""<div style="{step_style}"><div style="width:48px; height:48px; margin:0 auto 10px; clip-path:polygon(50% 0, 0% 100%, 100% 100%); background:linear-gradient(180deg,{colors['accent']}, {colors['warning']});"></div><div style="font-weight:700; color:{colors['text']};">Share & lead</div><div style="color:{colors['text_secondary']}; font-size:13px; margin-top:6px;">Use our materials to run a session or share tips with friends and classmates.</div></div>""", unsafe_allow_html=True)
    
    # Features row (three cards) — inserted from user attachment
    st.markdown(
        f"""
        <div style="margin-top:18px; margin-bottom:8px;">
          <div style="font-size:18px; font-weight:800; color: {colors['text']};">What you can do</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    fcol1, fcol2, fcol3 = st.columns([1, 1, 1], gap="large")

    with fcol1:
        st.markdown(
            f"""
            <div class="hf-card" style="padding:18px; text-align:center;">
              <div style="width:84px; height:84px; margin:0 auto 12px; border-radius:12px; background:{colors['card_bg']}; display:flex; align-items:center; justify-content:center;">
                <!-- square icon -->
                <div style="width:36px; height:36px; background:linear-gradient(180deg,{colors['accent']}, {colors['secondary']}); border-radius:6px;"></div>
              </div>
              <div style="font-weight:700; color: {colors['text']};">AI fact checker.</div>
              <div style="color: {colors['text_secondary']}; font-size:13px; margin-top:6px;">Instantly check health claims and news for validity using advanced AI analysis.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with fcol2:
        st.markdown(
            f"""
            <div class="hf-card" style="padding:18px; text-align:center;">
              <div style="width:84px; height:84px; margin:0 auto 12px; border-radius:12px; background:{colors['card_bg']}; display:flex; align-items:center; justify-content:center;">
                <!-- circle icon -->
                <div style="width:36px; height:36px; background:radial-gradient(circle at 40% 30%, {colors['accent']}, {colors['success']}); border-radius:50%;"></div>
              </div>
              <div style="font-weight:700; color: {colors['text']};">Quiz &amp; games.</div>
              <div style="color: {colors['text_secondary']}; font-size:13px; margin-top:6px;">Interactive quizzes and mini-games boost your health knowledge and retention.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with fcol3:
        st.markdown(
            f"""
            <div class="hf-card" style="padding:18px; text-align:center;">
              <div style="width:84px; height:84px; margin:0 auto 12px; border-radius:12px; background:{colors['card_bg']}; display:flex; align-items:center; justify-content:center;">
                <!-- triangle icon -->
                <div style="width:0; height:0; border-left:18px solid transparent; border-right:18px solid transparent; border-bottom:32px solid {colors['accent']}; transform:translateY(6px);"></div>
              </div>
              <div style="font-weight:700; color: {colors['text']};">Progress tracking.</div>
              <div style="color: {colors['text_secondary']}; font-size:13px; margin-top:6px;">Monitor your learning streak, badges, and daily insights as you grow healthier.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # (compact icon row removed)

    # (Target audience moved into right column card)

    # CTA
    st.markdown("<div style='text-align: center; margin: 24px 0;'>", unsafe_allow_html=True)
    if st.button("Start Fact-Checking", key="landing-cta", use_container_width=True, type="primary"):
        set_page("Auth")
    st.markdown("</div>", unsafe_allow_html=True)
