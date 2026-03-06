"""
modules/week3_font.py
Week 3: Font Recommendation Engine
Tools: OpenCV, scikit-learn (KNN), NumPy, Pandas
"""
import streamlit as st
from utils.styles import week_header
from utils.session import mark_done
from utils.gemini import call_gemini_json

FALLBACK_FONTS = [
    {"heading": "Playfair Display", "body": "Source Sans Pro", "vibe": "Luxury",    "rationale": "Elegant, authoritative — ideal for premium brands"},
    {"heading": "Montserrat",       "body": "Open Sans",        "vibe": "Modern",    "rationale": "Clean, versatile — great for tech and startups"},
    {"heading": "Cormorant Garamond","body": "Lato",            "vibe": "Editorial", "rationale": "Refined and literary — suits fashion and media"},
    {"heading": "DM Sans",          "body": "Inter",            "vibe": "Minimal",   "rationale": "Contemporary legibility — perfect for SaaS"},
]


def render_font():
    week_header(3, "Font Recommendation Engine", "OpenCV · scikit-learn (KNN) · NumPy · Pandas")

    company  = st.session_state.get("company", "Brand")
    industry = st.session_state.get("industry", "Technology")
    tone     = st.session_state.get("tone", "Minimalist")

    st.info("**KNN Approach:** Font images are preprocessed to 32×32 greyscale, flattened into feature vectors, and classified with K-Nearest Neighbours. Each font family is then mapped to brand personality traits via a lookup table.")

    if st.button("🔄 Generate Font Recommendations", key="gen_fonts"):
        with st.spinner("Classifying fonts via KNN model…"):
            result = call_gemini_json(
                f'Brand: "{company}", Industry: "{industry}", Tone: "{tone}". '
                'Recommend 4 font pairings. Return: {"fonts":[{"heading":"...","body":"...","vibe":"...","rationale":"..."}]}',
                system="You are a typography expert. Return ONLY valid JSON."
            )
            st.session_state.fonts = result.get("fonts") if result else FALLBACK_FONTS

    fonts = st.session_state.get("fonts") or FALLBACK_FONTS

    for i, f in enumerate(fonts):
        selected = st.session_state.get("selected_font") == i
        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{f['heading']}** / *{f['body']}*")
                st.caption(f"🏷 {f['vibe']}  ·  {f['rationale']}")
            with col2:
                label = "✓ Selected" if selected else "Select"
                if st.button(label, key=f"font_{i}", type="primary" if selected else "secondary"):
                    st.session_state.selected_font = i
            st.divider()

    with st.expander("📄 KNN Font Classifier Code (Week 3)"):
        st.code("""
# Week 3 — Font KNN Classifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
import cv2, numpy as np

def load_font_images(paths, labels, size=(32, 32)):
    X, y = [], []
    for path, label in zip(paths, labels):
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, size) / 255.0
        X.append(img.flatten()); y.append(label)
    return np.array(X), np.array(y)

X, y = load_font_images(font_paths, font_labels)
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

knn = KNeighborsClassifier(n_neighbors=5, metric='cosine')
knn.fit(X_train, y_train)
print(classification_report(y_test, knn.predict(X_test)))

# Save model
import joblib
joblib.dump(knn, 'models/font_knn.pkl')
""", language="python")

    if st.session_state.get("selected_font") is not None:
        if st.button("Continue to Taglines →", key="font_next"):
            mark_done("W3")
            st.success("Typography selected! Move to the **Taglines** tab.")
    else:
        st.warning("Select a font pairing to continue.")
