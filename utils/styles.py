"""utils/styles.py — Global CSS for BrandMind AI Streamlit app"""
import streamlit as st


def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root tokens ── */
:root {
    --gold: #b8975a;
    --dark: #1a1a18;
    --cream: #f5f0e8;
    --surface: #ffffff;
    --border: rgba(0,0,0,0.08);
    --text2: #6b6a65;
}

/* ── Typography ── */
h1, h2, h3 { font-family: 'DM Serif Display', Georgia, serif !important; letter-spacing: -0.02em; }
body, p, div { font-family: 'DM Sans', system-ui, sans-serif !important; }

/* ── Hide default streamlit chrome ── */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Main container ── */
.main .block-container { padding-top: 1.5rem; padding-bottom: 4rem; max-width: 860px; }

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: #f5f0e8;
    border: 1px solid rgba(0,0,0,0.07);
    border-radius: 12px;
    padding: 14px 18px;
}
[data-testid="metric-container"] label { font-size: 0.72rem !important; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text2) !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { font-family: 'DM Serif Display', Georgia, serif !important; font-size: 1.8rem !important; }

/* ── Buttons ── */
.stButton > button {
    background: #1a1a18 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 99px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    padding: 0.5rem 1.4rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover { transform: translateY(-1px) !important; box-shadow: 0 4px 16px rgba(0,0,0,0.22) !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: #f0ede8;
    border-radius: 99px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 99px !important;
    font-size: 0.8rem !important;
    font-weight: 450 !important;
    color: #6b6a65 !important;
    padding: 6px 14px !important;
}
.stTabs [aria-selected="true"] {
    background: #ffffff !important;
    color: #1a1a18 !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08) !important;
}

/* ── Expander ── */
.streamlit-expanderHeader { font-weight: 500 !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] { background: #1a1a18 !important; }
[data-testid="stSidebar"] * { color: #f5f0e8 !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.1) !important; }

/* ── Info / success boxes ── */
.stAlert { border-radius: 10px !important; }

/* ── Gold badge ── */
.gold-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: #f5edd8; color: #b8975a;
    font-size: 0.7rem; font-weight: 600; letter-spacing: 0.1em;
    text-transform: uppercase; padding: 4px 12px;
    border-radius: 99px; margin-bottom: 8px;
}

/* ── Week header ── */
.week-header {
    background: #1a1a18; color: #f5f0e8;
    border-radius: 10px; padding: 12px 18px;
    margin-bottom: 18px; display: flex;
    align-items: center; justify-content: space-between;
}
.week-header .wh-num { color: #b8975a; font-weight: 700; font-size: 0.8rem; }
.week-header .wh-title { font-family: 'DM Serif Display', serif; font-size: 1.05rem; }
.week-header .wh-tools { font-size: 0.72rem; opacity: 0.55; }

/* ── Colour swatch inline ── */
.swatch-row { display: flex; gap: 8px; flex-wrap: wrap; margin: 8px 0; }
.swatch-block { width: 40px; height: 40px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.12); cursor: pointer; transition: transform 0.2s; }
.swatch-block:hover { transform: scale(1.12); }
</style>
""", unsafe_allow_html=True)


def week_header(n: int, title: str, tools: str):
    st.markdown(f"""
<div class="week-header">
  <div>
    <div class="wh-num">WEEK {n}</div>
    <div class="wh-title">{title}</div>
  </div>
  <div class="wh-tools">{tools}</div>
</div>""", unsafe_allow_html=True)
