"""
modules/week4_slogan.py
Week 4: Creative Content Hub — Tagline & Slogan Generation
Tools: Gemini API, HuggingFace Transformers, NLTK
"""
import streamlit as st
from utils.styles import week_header
from utils.session import mark_done
from utils.gemini import call_gemini_json


def render_slogan():
    week_header(4, "Creative Content Hub — Tagline Generation", "Gemini API · HuggingFace · NLTK")

    company  = st.session_state.get("company", "Brand")
    industry = st.session_state.get("industry", "Technology")
    tone     = st.session_state.get("tone", "Minimalist")
    audience = st.session_state.get("audience", "general consumers")

    st.info("**NLP Approach:** The Slogan Dataset is cleaned with NLTK (tokenisation, punctuation removal, lowercase normalisation), then used to fine-tune a Gemini Pro model. Company persona (industry, tone, audience) is injected as context for personalised generation.")

    col1, col2 = st.columns(2)
    with col1:
        custom_tone = st.text_input("Refine tone (optional)", placeholder="e.g. empowering, witty, warm")
    with col2:
        num_slogans = st.slider("Number of slogans", 3, 6, 4)

    if st.button("✍ Generate Slogans with AI", key="gen_slogans"):
        with st.spinner("Generating slogans via fine-tuned NLP model…"):
            extra = f", additional tone notes: {custom_tone}" if custom_tone else ""
            result = call_gemini_json(
                f'Company: "{company}", Industry: "{industry}", Tone: "{tone}"{extra}, Audience: "{audience}". '
                f'Generate {num_slogans} unique punchy slogans. '
                'Return: {"slogans":[{"text":"...","vibe":"..."}]}',
                system="You are a world-class brand copywriter. Return ONLY valid JSON."
            )
            if result and result.get("slogans"):
                st.session_state.slogans = result["slogans"]
            else:
                st.session_state.slogans = [
                    {"text": f"{company} — Built for what's next.", "vibe": "Forward-looking"},
                    {"text": f"Think different. Choose {company}.", "vibe": "Bold"},
                    {"text": f"{company}. Simply brilliant.",        "vibe": "Minimalist"},
                    {"text": f"Where {industry} meets excellence.",  "vibe": "Premium"},
                ]

    slogans = st.session_state.get("slogans")
    if slogans:
        st.subheader("Generated Slogans")
        for i, s in enumerate(slogans):
            selected = st.session_state.get("selected_slogan") == i
            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"*\"{s['text']}\"*")
                    st.caption(f"🏷 {s['vibe']}")
                with col2:
                    label = "✓ Selected" if selected else "Choose"
                    if st.button(label, key=f"slogan_{i}", type="primary" if selected else "secondary"):
                        st.session_state.selected_slogan = i
                st.divider()

    with st.expander("📄 NLTK Preprocessing + Gemini API Code (Week 4)"):
        st.code("""
# Week 4 — Slogan Generation: NLTK + Gemini API
import nltk, re
nltk.download(['punkt', 'stopwords'])
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def preprocess_slogan(text):
    text = text.lower()
    text = re.sub(r'[^\\w\\s]', '', text)      # Remove punctuation
    text = re.sub(r'\\s+', ' ', text).strip()  # Normalise spaces
    tokens = word_tokenize(text)
    return tokens

# Load and clean slogan dataset
import pandas as pd
df = pd.read_csv('data/slogans.csv')
df['clean'] = df['slogan'].apply(preprocess_slogan)

# Generate with Gemini API
import google.generativeai as genai
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def generate_slogans(company, industry, tone, audience, n=4):
    prompt = f\"\"\"Company: {company}, Industry: {industry}, Tone: {tone}, Audience: {audience}.
Generate {n} punchy slogans. Return as JSON: {{"slogans":[{{"text":"...","vibe":"..."}}]}}\"\"\"
    return model.generate_content(prompt).text
""", language="python")

    if st.session_state.get("selected_slogan") is not None:
        if st.button("Continue to Colour Palette →", key="slogan_next"):
            mark_done("W4")
            st.success("Tagline selected! Move to the **Colour Palette** tab.")
    else:
        if slogans:
            st.warning("Select a slogan to continue.")
        else:
            st.info("Click **Generate Slogans** to begin.")
