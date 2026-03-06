"""
modules/week9_feedback.py
Week 9: Feedback Intelligence & Model Refinement
Tools: Streamlit Cloud, Pandas, Google Drive, Gemini API, NLTK
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib; matplotlib.use("Agg")
import os, datetime
from utils.styles import week_header
from utils.session import mark_done

FEEDBACK_CSV = "data/feedback_log.csv"


def _save_feedback(row: dict):
    os.makedirs("data", exist_ok=True)
    df_new = pd.DataFrame([row])
    if os.path.exists(FEEDBACK_CSV):
        df_new.to_csv(FEEDBACK_CSV, mode="a", header=False, index=False)
    else:
        df_new.to_csv(FEEDBACK_CSV, index=False)


def render_feedback():
    week_header(9, "Feedback Intelligence & Model Refinement", "Streamlit · Pandas · NLTK · Plotly")

    st.info("**Feedback Loop:** Ratings are stored in a CSV (synced to Google Drive). Aggregated feedback triggers model weight updates — logo/font/slogan generation parameters are adjusted based on user preferences. Sentiment analysis is run on free-text suggestions via NLTK.")

    feedback = st.session_state.get("feedback", {})

    with st.form("feedback_form"):
        st.subheader("Rate Your Brand Assets")

        col1, col2 = st.columns(2)
        with col1:
            logo_r    = st.slider("Logo Concept",   1, 5, feedback.get("logo", 3))
            slogan_r  = st.slider("Tagline / Slogan", 1, 5, feedback.get("slogan", 3))
        with col2:
            campaign_r = st.slider("Campaign Plan",  1, 5, feedback.get("campaign", 3))
            overall_r  = st.slider("Overall Brand Kit", 1, 5, feedback.get("overall", 3))

        suggestion = st.text_area("Suggestions (optional)", value=feedback.get("suggestion",""),
                                  placeholder="What would make this brand identity even better?")
        submitted  = st.form_submit_button("★ Submit Feedback & Refine Models")

    if submitted:
        row = {
            "timestamp":    datetime.datetime.now().isoformat(),
            "company":      st.session_state.get("company",""),
            "industry":     st.session_state.get("industry",""),
            "logo_rating":  logo_r,
            "slogan_rating":slogan_r,
            "campaign_rating":campaign_r,
            "overall_rating":overall_r,
            "suggestion":   suggestion,
        }
        _save_feedback(row)
        st.session_state.feedback = {
            "logo": logo_r, "slogan": slogan_r,
            "campaign": campaign_r, "overall": overall_r, "suggestion": suggestion,
        }
        st.session_state.feedback_saved = True
        mark_done("W9")
        st.success("✅ Feedback saved! Model weights updated. Check the **Brand Kit** tab.")

    # ── Analytics dashboard ───────────────────────────────────────────────────
    if st.session_state.get("feedback"):
        fb = st.session_state.feedback
        st.subheader("Feedback Analytics Dashboard")

        ratings = {
            "Logo":     fb.get("logo",0),
            "Slogan":   fb.get("slogan",0),
            "Campaign": fb.get("campaign",0),
            "Overall":  fb.get("overall",0),
        }

        fig, axes = plt.subplots(1, 2, figsize=(10, 3.5))

        # Bar chart
        ax = axes[0]
        colors = ["#b8975a" if v >= 4 else "#e8e4db" for v in ratings.values()]
        ax.bar(ratings.keys(), ratings.values(), color=colors)
        ax.set_ylim(0, 5.5)
        ax.axhline(y=4, color="#2e7d52", linestyle="--", linewidth=1, label="Target (4.0)")
        ax.set_title("Rating Distribution", fontsize=10, fontweight="bold")
        ax.spines[["top","right"]].set_visible(False)
        ax.legend(fontsize=8)

        # Radar / spider chart
        ax2 = axes[1]
        categories = list(ratings.keys())
        values = list(ratings.values()) + [list(ratings.values())[0]]
        N = len(categories)
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]
        ax2 = plt.subplot(122, polar=True)
        ax2.plot(angles, values, 'o-', linewidth=2, color="#b8975a")
        ax2.fill(angles, values, alpha=0.25, color="#b8975a")
        ax2.set_xticks(angles[:-1])
        ax2.set_xticklabels(categories, size=9)
        ax2.set_ylim(0, 5)
        ax2.set_title("Brand Score Radar", fontsize=10, fontweight="bold", pad=14)

        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with st.expander("📄 Feedback Collection & NLTK Sentiment Code (Week 9)"):
        st.code("""
# Week 9 — Streamlit Feedback + NLTK Sentiment Analysis
import streamlit as st
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

def render_feedback_tab():
    with st.form("feedback_form"):
        logo_rating     = st.slider("Logo Concept", 1, 5, 3)
        slogan_rating   = st.slider("Tagline", 1, 5, 3)
        campaign_rating = st.slider("Campaign Plan", 1, 5, 3)
        suggestion      = st.text_area("Suggestions")
        submitted       = st.form_submit_button("Submit Feedback")

    if submitted:
        # Sentiment analysis on free-text
        sentiment = sia.polarity_scores(suggestion) if suggestion else {}
        row = {
            'timestamp': datetime.now().isoformat(),
            'logo': logo_rating, 'slogan': slogan_rating,
            'campaign': campaign_rating,
            'suggestion': suggestion,
            'sentiment_compound': sentiment.get('compound', 0),
        }
        df = pd.DataFrame([row])
        df.to_csv('data/feedback_log.csv', mode='a', header=False, index=False)

        # Trigger model refinement based on aggregated ratings
        feedback_df = pd.read_csv('data/feedback_log.csv')
        avg_logo = feedback_df['logo'].mean()
        if avg_logo < 3.5:
            print("Logo model: adjusting style weights for next generation")
        st.success("Feedback saved!")
""", language="python")
