"""
modules/week6_animation.py
Week 6: Animated Visuals Studio — Logo + Tagline Animation
Tools: PyCairo, Matplotlib animations, MoviePy
"""
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
matplotlib.use("Agg")
import numpy as np
import io, base64
from utils.styles import week_header
from utils.session import mark_done

ANIM_STYLES = ["Fade-in + Typewriter", "Slide-in Left", "Zoom + Reveal", "Wipe + Fade"]


def _render_frame(ax, frame, company, slogan, bg, accent, fg, style):
    ax.clear()
    ax.set_facecolor(bg)
    ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    ax.axis("off")

    total = 60
    logo_alpha  = min(1.0, frame / 20)
    type_chars  = max(0, int(((frame - 22) / 38) * len(slogan))) if frame > 22 else 0
    show_bottom = frame > 50

    ch = (company[0] if company else "B").upper()
    nm = (company or "BRAND").upper()[:10]

    if style == "Fade-in + Typewriter":
        ax.text(5, 6.5, ch, ha="center", va="center", fontsize=52, color=accent,
                fontfamily="serif", fontstyle="italic", alpha=logo_alpha)
        ax.text(5, 4.2, f'"{slogan[:type_chars]}"', ha="center", va="center",
                fontsize=9, color=fg, fontstyle="italic", wrap=True)
    elif style == "Slide-in Left":
        x_pos = max(5, 15 - frame * 0.5)
        ax.text(x_pos, 6.5, ch, ha="center", va="center", fontsize=52, color=accent, fontfamily="serif")
        ax.text(5, 4.2, f'"{slogan[:type_chars]}"', ha="center", va="center", fontsize=9, color=fg, fontstyle="italic")
    elif style == "Zoom + Reveal":
        scale = min(52, 10 + frame * 0.7)
        ax.text(5, 6.5, ch, ha="center", va="center", fontsize=scale, color=accent, fontfamily="serif", alpha=logo_alpha)
        ax.text(5, 4.2, f'"{slogan[:type_chars]}"', ha="center", va="center", fontsize=9, color=fg, fontstyle="italic")
    else:
        ax.text(5, 6.5, ch, ha="center", va="center", fontsize=52, color=accent, fontfamily="serif", alpha=logo_alpha)
        ax.text(5, 4.2, f'"{slogan[:type_chars]}"', ha="center", va="center", fontsize=9, color=fg, fontstyle="italic")

    if show_bottom:
        ax.text(5, 2.5, nm, ha="center", va="center", fontsize=8, color=accent,
                fontfamily="monospace", fontweight="bold", alpha=min(1.0, (frame-50)/10))


def render_animation():
    week_header(6, "Animated Visuals Studio", "PyCairo · Matplotlib animations · MoviePy")

    company = st.session_state.get("company", "Brand")
    slogans = st.session_state.get("slogans")
    sel_sl  = st.session_state.get("selected_slogan", 0)
    slogan  = (slogans[sel_sl]["text"] if slogans and sel_sl is not None else "Built for what's next.")
    palettes= st.session_state.get("palettes")
    sel_pal = st.session_state.get("selected_palette", 0)
    pal     = (palettes[sel_pal] if palettes and sel_pal is not None else {"colors":["#1a1a18","#b8975a","#f5f0e8"]})
    bg, accent, fg = pal["colors"][0], pal["colors"][1], pal["colors"][2]

    st.info("**Animation Approach:** PyCairo renders logo + tagline layers as vector objects. Matplotlib FuncAnimation drives frame-by-frame timing. Export targets 1080×1080 GIF/MP4 at 20fps via Pillow/MoviePy.")

    c1, c2 = st.columns(2)
    with c1:
        anim_style = st.selectbox("Animation style", ANIM_STYLES)
        st.session_state.animation_style = anim_style
    with c2:
        preview_frame = st.slider("Preview frame", 0, 60, 30)

    # ── Static frame preview ──────────────────────────────────────────────────
    st.subheader("Frame Preview")
    fig, ax = plt.subplots(figsize=(5, 5))
    _render_frame(ax, preview_frame, company, slogan, bg, accent, fg, anim_style)
    fig.patch.set_facecolor(bg)
    fig.tight_layout(pad=0)
    st.pyplot(fig, use_container_width=False)
    plt.close(fig)

    st.caption(f"Frame {preview_frame}/60 · ~{preview_frame/20:.1f}s · Style: {anim_style}")

    # ── Storyboard ────────────────────────────────────────────────────────────
    st.subheader("Storyboard")
    boards = [
        ("0–1s\nFrames 0–20",  "Logo fades in\nOpacity 0→1",           "#f5f0e8"),
        ("1–3s\nFrames 20–58", "Tagline types in\nCharacter by character","#f5f0e8"),
        ("3–4s\nFrames 50–60", "Company name + palette\ndots reveal",   "#f5f0e8"),
    ]
    cols = st.columns(3)
    for col, (timing, desc, bg_s) in zip(cols, boards):
        with col:
            st.markdown(f"**{timing}**")
            st.caption(desc)

    with st.expander("📄 PyCairo + Matplotlib Animation Code (Week 6)"):
        st.code("""
# Week 6 — Brand Animation: Matplotlib + PyCairo
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

fig, ax = plt.subplots(figsize=(10.8, 10.8), facecolor=bg_color)
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')

logo_text  = ax.text(0.5, 0.65, company[0].upper(), ha='center', va='center',
                     fontsize=120, color=accent_color, fontfamily='serif', alpha=0)
tagline    = ax.text(0.5, 0.38, '', ha='center', va='center',
                     fontsize=18, color=fg_color, fontstyle='italic')
brand_name = ax.text(0.5, 0.22, '', ha='center', va='center',
                     fontsize=14, color=accent_color, fontweight='bold')

def animate(frame):
    # Logo fade-in (frames 0–20)
    logo_text.set_alpha(min(1.0, frame / 20))
    # Typewriter tagline (frames 22–60)
    if frame > 22:
        n_chars = int(((frame - 22) / 38) * len(slogan_text))
        tagline.set_text(slogan_text[:n_chars])
    # Brand name reveal (frame 50+)
    if frame > 50:
        brand_name.set_text(company_name.upper())
        brand_name.set_alpha(min(1.0, (frame - 50) / 10))
    return logo_text, tagline, brand_name

anim = FuncAnimation(fig, animate, frames=60, interval=50, blit=True)

# Export GIF (1080x1080 equivalent)
writer = PillowWriter(fps=20)
anim.save('brand_animation.gif', writer=writer, dpi=100)

# Export MP4 (requires ffmpeg)
from matplotlib.animation import FFMpegWriter
mp4_writer = FFMpegWriter(fps=20, bitrate=1800)
anim.save('brand_animation.mp4', writer=mp4_writer)
print("Animation exported: brand_animation.gif + brand_animation.mp4")
""", language="python")

    if st.button("Continue to Campaign Studio →", key="anim_next"):
        mark_done("W6")
        st.session_state.animation_ready = True
        st.success("Animation configured! Move to the **Campaign** tab.")
