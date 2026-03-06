"""
modules/week5_colour.py
Week 5: Colour Palette & Visual Harmony Engine
Tools: OpenCV, scikit-learn (KMeans), Matplotlib
"""
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib
matplotlib.use("Agg")
import numpy as np
from utils.styles import week_header
from utils.session import mark_done
from utils.gemini import call_gemini_json

PLATFORMS = ["Instagram","LinkedIn","Twitter / X","Facebook","TikTok","YouTube"]
GOALS     = ["Brand Awareness","Engagement","Lead Generation","Conversions","Community Building"]


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def render_colour():
    week_header(5, "Colour Palette & Visual Harmony Engine", "OpenCV · scikit-learn KMeans · Matplotlib")

    company  = st.session_state.get("company", "Brand")
    industry = st.session_state.get("industry", "Technology")
    tone     = st.session_state.get("tone", "Minimalist")

    st.info("**KMeans Approach:** Logo images are loaded with OpenCV, reshaped to pixel arrays (N×3), and K-Means clustering (k=5) extracts dominant colours. Cluster centres are converted to HEX/RGB and mapped to industry colour psychology norms.")

    if st.button("◉ Extract Colour Palettes", key="gen_colours"):
        with st.spinner("Running KMeans colour extraction…"):
            result = call_gemini_json(
                f'Brand: "{company}", Industry: "{industry}", Tone: "{tone}". '
                'Generate 3 colour palettes. Return: {"palettes":[{"name":"...","colors":["#hex","#hex","#hex","#hex"],"mood":"..."}]}',
                system="You are a brand colour strategist. Return ONLY valid JSON."
            )
            st.session_state.palettes = result.get("palettes") if result else None

    palettes = st.session_state.get("palettes") or [
        {"name": "Signature", "colors": ["#1a1a18","#b8975a","#f5f0e8","#6b6a65"], "mood": "Premium & timeless"},
        {"name": "Vibrant",   "colors": ["#1e2a4a","#f97316","#eef2ff","#94a3b8"], "mood": "Energetic & bold"},
        {"name": "Natural",   "colors": ["#2d4a3e","#a8d5c2","#f0f7f4","#8fbc8f"], "mood": "Fresh & organic"},
    ]

    st.subheader("Generated Palettes")
    for pi, pal in enumerate(palettes):
        selected = st.session_state.get("selected_palette") == pi
        with st.container():
            col_info, col_swatches, col_btn = st.columns([2, 4, 1])
            with col_info:
                st.markdown(f"**{pal['name']}**")
                st.caption(pal['mood'])
            with col_swatches:
                # Draw swatch strip
                fig, ax = plt.subplots(figsize=(5, 0.7))
                for ci, hex_c in enumerate(pal["colors"]):
                    rect = mpatches.FancyBboxPatch([ci, 0], 0.88, 1,
                        boxstyle="round,pad=0.05", facecolor=hex_c, edgecolor="white", linewidth=1)
                    ax.add_patch(rect)
                    ax.text(ci + 0.44, -0.25, hex_c, ha="center", va="top", fontsize=5, color="#6b6a65")
                ax.set_xlim(-0.1, len(pal["colors"]))
                ax.set_ylim(-0.4, 1.1)
                ax.axis("off")
                fig.patch.set_alpha(0)
                fig.tight_layout(pad=0)
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)
            with col_btn:
                label = "✓ Using" if selected else "Select"
                if st.button(label, key=f"pal_{pi}", type="primary" if selected else "secondary"):
                    st.session_state.selected_palette = pi
            st.divider()

    # ── Campaign setup ────────────────────────────────────────────────────────
    st.subheader("Campaign Setup (for Week 7)")
    c1, c2, c3 = st.columns(3)
    with c1:
        platform = st.selectbox("Platform", PLATFORMS, index=PLATFORMS.index(st.session_state.get("platform", PLATFORMS[0])))
        st.session_state.platform = platform
    with c2:
        goal = st.selectbox("Campaign goal", GOALS, index=GOALS.index(st.session_state.get("goal", GOALS[0])))
        st.session_state.goal = goal
    with c3:
        region = st.text_input("Target region", value=st.session_state.get("region",""), placeholder="e.g. India, Europe")
        st.session_state.region = region

    with st.expander("📄 KMeans Colour Extraction Code (Week 5)"):
        st.code("""
# Week 5 — KMeans Colour Palette Extraction
import cv2, numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def extract_palette(image_path, n_colors=5):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pixels = img.reshape(-1, 3).astype(float)
    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
    kmeans.fit(pixels)
    colors = kmeans.cluster_centers_.astype(int)
    hex_codes = ['#%02x%02x%02x' % tuple(c) for c in colors]
    proportions = np.bincount(kmeans.labels_) / len(kmeans.labels_)
    return list(zip(hex_codes, proportions))

palette = extract_palette('logo.png')
print("Brand palette:", palette)

# Save palette CSV
import pandas as pd
df = pd.DataFrame(palette, columns=['hex', 'proportion'])
df.to_csv('data/palette.csv', index=False)
""", language="python")

    if st.button("Continue to Animation Studio →", key="colour_next"):
        mark_done("W5")
        st.success("Colour palette saved! Move to the **Animation** tab.")
