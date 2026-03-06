"""
BrandMind AI — AI-Powered Automated Branding Assistant
CRS AI Capstone 2025-26 | Scenario 1
Week 10: Integration & Streamlit Cloud Deployment
"""

import streamlit as st

st.set_page_config(
    page_title="BrandMind AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Import all modules ────────────────────────────────────────────────────────
from modules.week1_eda        import render_eda
from modules.week2_logo       import render_logo
from modules.week3_font       import render_font
from modules.week4_slogan     import render_slogan
from modules.week5_colour     import render_colour
from modules.week6_animation  import render_animation
from modules.week7_campaign   import render_campaign
from modules.week8_multilang  import render_multilang
from modules.week9_feedback   import render_feedback
from modules.week10_kit       import render_kit
from utils.styles             import inject_css
from utils.session            import init_session

# ── Init ──────────────────────────────────────────────────────────────────────
inject_css()
init_session()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ✦ BrandMind AI")
    st.markdown("*AI-Powered Branding Assistant*")
    st.divider()
    if st.session_state.get("company"):
        st.markdown(f"**Brand:** {st.session_state.company}")
        st.markdown(f"**Industry:** {st.session_state.get('industry','—')}")
        st.markdown(f"**Tone:** {st.session_state.get('tone','—')}")
        st.divider()
    st.markdown("**Modules**")
    weeks = [
        ("W1","Dataset EDA"),("W2","Logo Studio"),("W3","Font Engine"),
        ("W4","Content Hub"),("W5","Colour Engine"),("W6","Animation Studio"),
        ("W7","Campaign Studio"),("W8","Multilingual"),("W9","Feedback AI"),("W10","Brand Kit"),
    ]
    for w, label in weeks:
        done = st.session_state.get(f"done_{w}", False)
        icon = "✅" if done else "○"
        st.markdown(f"{icon} {w}: {label}")
    st.divider()
    st.caption("CRS AI Capstone 2025-26 · Scenario 1")

# ── Main tabs ─────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "✦ Setup & EDA",
    "◈ Logo Studio",
    "Aa Font Engine",
    "✍ Taglines",
    "◉ Colour Palette",
    "▶ Animation",
    "📈 Campaign",
    "🌐 Multilingual",
    "★ Feedback",
    "⬇ Brand Kit",
])

with tabs[0]:  render_eda()
with tabs[1]:  render_logo()
with tabs[2]:  render_font()
with tabs[3]:  render_slogan()
with tabs[4]:  render_colour()
with tabs[5]:  render_animation()
with tabs[6]:  render_campaign()
with tabs[7]:  render_multilang()
with tabs[8]:  render_feedback()
with tabs[9]:  render_kit()
