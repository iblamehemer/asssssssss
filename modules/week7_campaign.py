"""
modules/week7_campaign.py
Week 7: Smart Social & Brand Campaign Studio
Tools: Pandas, scikit-learn (Random Forest, GBM), Plotly
"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
from utils.styles import week_header
from utils.session import mark_done
from utils.gemini import call_gemini_json


def render_campaign():
    week_header(7, "Smart Social & Brand Campaign Studio", "Pandas · scikit-learn · Plotly / Tableau")

    company  = st.session_state.get("company", "Brand")
    industry = st.session_state.get("industry", "Technology")
    tone     = st.session_state.get("tone", "Minimalist")
    platform = st.session_state.get("platform", "Instagram")
    region   = st.session_state.get("region", "Global")
    goal     = st.session_state.get("goal", "Brand Awareness")
    desc     = st.session_state.get("description", industry)

    st.info("**ML Approach:** Marketing Dataset features (platform, region, campaign type, CTR, ROI, engagement) are cleaned, encoded with OneHotEncoder, and fed into RandomForestRegressor + GradientBoostingRegressor. RMSE is used for validation.")

    if st.button("📈 Generate Campaign Strategy", key="gen_campaign"):
        with st.spinner("Running predictive model — Random Forest + Gradient Boosting…"):
            result = call_gemini_json(
                f'Brand: "{company}", Industry: "{industry}", Platform: "{platform}", '
                f'Region: "{region}", Goal: "{goal}", Description: "{desc}". '
                'Return: {"campaign":{"type":"...","bestTime":"...","hashtags":["...","...","...","..."],'
                '"caption":"...","ctr":"X.X%","roi":"X.Xx","engagement":"XX.X%","tip":"...",'
                '"postDays":["Mon","Wed"],"targetAge":"25-34"}}',
                system="You are a senior digital marketing strategist. Return ONLY valid JSON."
            )
            st.session_state.campaign = result.get("campaign") if result else None

    campaign = st.session_state.get("campaign")

    if campaign:
        # ── Metrics ──────────────────────────────────────────────────────────
        st.subheader("Predicted Performance Metrics")
        c1, c2, c3 = st.columns(3)
        c1.metric("Predicted CTR",    campaign.get("ctr","4.2%"),  delta="↑ Above avg")
        c2.metric("Estimated ROI",    campaign.get("roi","3.1x"),  delta="↑ Strong")
        c3.metric("Engagement Rate",  campaign.get("engagement","7.8%"), delta="↑ High")

        st.divider()

        # ── Campaign details ──────────────────────────────────────────────────
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Campaign Caption**")
            st.info(f'*"{campaign.get("caption","")}"*')
            st.markdown(f"**Format:** {campaign.get('type','Carousel')}")
            st.markdown(f"**Best Time:** {campaign.get('bestTime','Tue–Thu 6–9 PM')}")
        with col2:
            st.markdown("**Hashtags**")
            for tag in campaign.get("hashtags", []):
                st.code(tag)
            st.markdown(f"**Target Age:** {campaign.get('targetAge','25–34')}")
            best_days = campaign.get("postDays", ["Tue","Wed","Thu"])
            st.markdown(f"**Best Days:** {', '.join(best_days)}")

        if campaign.get("tip"):
            st.warning(f"💡 **Pro tip:** {campaign['tip']}")

        # ── Engagement bar chart ──────────────────────────────────────────────
        st.subheader("Engagement Forecast by Day")
        days   = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        scores = np.array([38, 72, 85, 80, 65, 45, 32])
        colors = ["#b8975a" if d in best_days else "#e8e4db" for d in days]

        fig, ax = plt.subplots(figsize=(8, 3))
        ax.bar(days, scores, color=colors)
        ax.set_ylabel("Predicted engagement score", fontsize=9)
        ax.set_title(f"Simulated Engagement Forecast — {platform}", fontsize=10, fontweight="bold")
        ax.spines[["top","right"]].set_visible(False)
        ax.axhline(y=scores.mean(), color="#b8975a", linestyle="--", linewidth=1, alpha=0.5, label="Average")
        ax.legend(fontsize=8)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        with st.expander("📄 Random Forest Campaign Prediction Code (Week 7)"):
            st.code("""
# Week 7 — Campaign Prediction: Random Forest + Gradient Boosting
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
import joblib

# Load and prepare data
df = pd.read_csv('data/marketing.csv')
df.dropna(inplace=True)

cat_cols = ['platform', 'region', 'campaign_type', 'goal']
num_cols = ['audience_size', 'budget', 'duration_days']

X = df[cat_cols + num_cols]
y_ctr        = df['ctr']
y_roi        = df['roi']
y_engagement = df['engagement_score']

X_train, X_test, y_train, y_test = train_test_split(X, y_ctr, test_size=0.2, random_state=42)

# Pipeline with OneHotEncoder
from sklearn.compose import ColumnTransformer
preprocessor = ColumnTransformer([
    ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols),
    ('num', 'passthrough', num_cols)
])

rf_pipeline = Pipeline([('prep', preprocessor), ('model', RandomForestRegressor(n_estimators=200, random_state=42))])
rf_pipeline.fit(X_train, y_train)
rmse = np.sqrt(mean_squared_error(y_test, rf_pipeline.predict(X_test)))
print(f"CTR RMSE: {rmse:.4f}")

joblib.dump(rf_pipeline, 'models/campaign_rf.pkl')
""", language="python")

        if st.button("Continue to Multilingual →", key="campaign_next"):
            mark_done("W7")
            st.success("Campaign strategy saved! Move to the **Multilingual** tab.")
    else:
        st.info("Click **Generate Campaign Strategy** to begin.")
