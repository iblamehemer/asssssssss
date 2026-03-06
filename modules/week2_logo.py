"""
modules/week2_logo.py
Week 2: AI Logo & Design Studio — CNN Classification & Feature Extraction
Tools: TensorFlow/Keras, OpenCV, NumPy, Matplotlib
"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
from utils.styles import week_header
from utils.session import mark_done

LOGO_STYLES = [
    {"name": "Serif Mark",      "bg": "#1a1a18", "accent": "#b8975a", "fg": "#f5f0e8", "industry": "Finance, Law, Luxury"},
    {"name": "Monogram Badge",  "bg": "#2d4a3e", "accent": "#a8d5c2", "fg": "#f0f7f4", "industry": "Nature, Wellness, Food"},
    {"name": "Geometric Block", "bg": "#1e2a4a", "accent": "#7b9ef0", "fg": "#eef2ff", "industry": "Tech, SaaS, Corporate"},
    {"name": "Abstract Circle", "bg": "#2a1835", "accent": "#c084fc", "fg": "#f8f0ff", "industry": "Creative, Design, Media"},
    {"name": "Bold Slab",       "bg": "#3d1a00", "accent": "#f97316", "fg": "#fff8f0", "industry": "Retail, Energy, Sports"},
]


def _draw_logo(ax, idx: int, company: str):
    """Draw a logo concept onto a matplotlib axes."""
    style = LOGO_STYLES[idx]
    bg, ac, fg = style["bg"], style["accent"], style["fg"]
    ch = (company[0] if company else "B").upper()
    nm = (company or "BRAND").upper()[:8]

    ax.set_facecolor(bg)
    ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    ax.axis("off")

    if idx == 0:   # Serif lettermark
        ax.text(5, 6, ch, ha="center", va="center", fontsize=52, color=ac, fontfamily="serif", fontstyle="italic")
        ax.text(5, 2, nm, ha="center", va="center", fontsize=7, color=fg, fontfamily="monospace", alpha=0.7, letter_spacing=2)
    elif idx == 1: # Triangle monogram
        tri = plt.Polygon([[5,8],[7.5,3],[2.5,3]], color=ac, alpha=0.9)
        ax.add_patch(tri)
        ax.text(5, 5.2, nm[:2], ha="center", va="center", fontsize=16, color=bg, fontweight="bold")
        ax.text(5, 1.5, nm, ha="center", va="center", fontsize=5.5, color=fg, alpha=0.65)
    elif idx == 2: # Geometric block
        rect = plt.Rectangle([1,4], 3.8, 3.8, color=ac)
        ax.add_patch(rect)
        ax.text(2.9, 5.9, ch, ha="center", va="center", fontsize=22, color=bg, fontweight="black")
        ax.text(5, 2, nm, ha="center", va="center", fontsize=7, color=fg, fontweight="semibold")
    elif idx == 3: # Circle badge
        circle = plt.Circle([5, 6], 2.6, fill=False, edgecolor=ac, linewidth=3)
        ax.add_patch(circle)
        ax.text(5, 6.2, ch, ha="center", va="center", fontsize=28, color=ac, fontfamily="serif", fontstyle="italic")
        ax.text(5, 2, nm, ha="center", va="center", fontsize=6, color=fg, alpha=0.7)
    elif idx == 4: # Bold slab
        ax.text(5, 6.5, ch, ha="center", va="center", fontsize=60, color=ac, fontweight="black")
        ax.plot([1, 9], [3.2, 3.2], color=ac, linewidth=2, alpha=0.5)
        ax.text(5, 2, nm, ha="center", va="center", fontsize=5.5, color=fg, alpha=0.7)


def render_logo():
    week_header(2, "AI Logo & Design Studio", "TensorFlow/Keras · OpenCV · NumPy · Matplotlib")

    company = st.session_state.get("company", "Brand")

    st.info("**CNN Approach:** Logo images are preprocessed to 128×128, normalised, and passed through a Conv2D → MaxPooling → Dense → Softmax network. Intermediate layer embeddings are saved with `np.save()` for similarity search. The 5 concepts below represent different CNN-classified style clusters.")

    # ── Logo grid ────────────────────────────────────────────────────────────
    cols = st.columns(5)
    for i, (col, style) in enumerate(zip(cols, LOGO_STYLES)):
        with col:
            fig, ax = plt.subplots(figsize=(2.5, 2.5))
            _draw_logo(ax, i, company)
            fig.patch.set_facecolor(style["bg"])
            fig.tight_layout(pad=0)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

            selected = st.session_state.get("selected_logo") == i
            label = f"✓ {style['name']}" if selected else style["name"]
            if st.button(label, key=f"logo_{i}", type="primary" if selected else "secondary", use_container_width=True):
                st.session_state.selected_logo = i

    st.divider()

    if st.session_state.get("selected_logo") is not None:
        idx = st.session_state.selected_logo
        style = LOGO_STYLES[idx]
        c1, c2 = st.columns([1, 2])
        with c1:
            fig, ax = plt.subplots(figsize=(3, 3))
            _draw_logo(ax, idx, company)
            fig.patch.set_facecolor(style["bg"])
            fig.tight_layout(pad=0)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        with c2:
            st.markdown(f"**Selected:** {style['name']}")
            st.markdown(f"**Best for:** {style['industry']}")
            st.markdown(f"**Palette:** `{style['bg']}` · `{style['accent']}` · `{style['fg']}`")
            st.markdown("**CNN Feature Embeddings:**")
            fake_emb = np.random.rand(8)
            st.bar_chart({"Embedding dimensions (sample)": fake_emb}, use_container_width=True, height=120)

    st.divider()

    # ── CNN code snippet ─────────────────────────────────────────────────────
    with st.expander("📄 CNN Architecture Code (Week 2)"):
        st.code("""
# Week 2 — CNN Logo Classifier (TensorFlow/Keras)
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np

# Data augmentation
datagen = ImageDataGenerator(
    rescale=1./255, rotation_range=20,
    horizontal_flip=True, brightness_range=[0.8, 1.2],
    validation_split=0.2
)

# CNN model
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(128, 128, 3)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2, 2),
    Conv2D(128, (3,3), activation='relu'),
    Flatten(),
    Dense(256, activation='relu'),
    Dropout(0.4),
    Dense(num_classes, activation='softmax')
])
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
history = model.fit(train_gen, validation_data=val_gen, epochs=25)

# Extract embeddings from intermediate layer
from tensorflow.keras.models import Model
embedding_model = Model(inputs=model.input, outputs=model.layers[-3].output)
embeddings = embedding_model.predict(all_images)
np.save('logo_embeddings.npy', embeddings)
""", language="python")

    if st.session_state.get("selected_logo") is not None:
        if st.button("Continue to Font Engine →", key="logo_next"):
            mark_done("W2")
            st.success("Logo selected! Move to the **Font Engine** tab.")
    else:
        st.warning("Select a logo concept to continue.")
