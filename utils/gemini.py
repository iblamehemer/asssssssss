"""utils/gemini.py — Gemini API wrapper for all AI generation tasks"""
import os
import json
import streamlit as st

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


def get_api_key() -> str:
    """Retrieve Gemini API key from Streamlit secrets or environment."""
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return os.getenv("GEMINI_API_KEY", "")


def call_gemini(prompt: str, system: str = "", temperature: float = 0.7, max_tokens: int = 1000) -> str:
    """
    Call Gemini Pro with a prompt. Returns text response.
    Falls back to a placeholder if API key is not configured.
    """
    api_key = get_api_key()

    if not GEMINI_AVAILABLE or not api_key:
        return _fallback(prompt)

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-pro",
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            ),
            system_instruction=system if system else None,
        )
        full_prompt = f"{system}\n\n{prompt}" if system and not model._system_instruction else prompt
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        st.warning(f"Gemini API error: {e}. Using fallback data.")
        return _fallback(prompt)


def call_gemini_json(prompt: str, system: str = "") -> dict | list | None:
    """Call Gemini and parse JSON response."""
    raw = call_gemini(prompt, system)
    try:
        clean = raw.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(clean)
    except Exception:
        return None


def _fallback(prompt: str) -> str:
    """Return sensible placeholder data when API is unavailable."""
    prompt_lower = prompt.lower()
    if "slogan" in prompt_lower or "tagline" in prompt_lower:
        return json.dumps({"slogans": [
            {"text": "Built for what's next.", "vibe": "Forward-looking"},
            {"text": "Simply brilliant.", "vibe": "Minimalist"},
            {"text": "Where excellence meets innovation.", "vibe": "Premium"},
            {"text": "The future, delivered today.", "vibe": "Bold"},
        ]})
    if "font" in prompt_lower or "typography" in prompt_lower:
        return json.dumps({"fonts": [
            {"heading": "Playfair Display", "body": "Source Sans Pro", "vibe": "Luxury", "rationale": "Elegant & authoritative"},
            {"heading": "Montserrat", "body": "Open Sans", "vibe": "Modern", "rationale": "Clean and versatile"},
            {"heading": "Cormorant Garamond", "body": "Lato", "vibe": "Editorial", "rationale": "Refined and literary"},
            {"heading": "DM Sans", "body": "Inter", "vibe": "Minimal", "rationale": "Contemporary and legible"},
        ]})
    if "colour" in prompt_lower or "palette" in prompt_lower or "color" in prompt_lower:
        return json.dumps({"palettes": [
            {"name": "Signature", "colors": ["#1a1a18", "#b8975a", "#f5f0e8", "#6b6a65"], "mood": "Premium & timeless"},
            {"name": "Vibrant",   "colors": ["#1e2a4a", "#f97316", "#eef2ff", "#94a3b8"], "mood": "Energetic & bold"},
            {"name": "Natural",   "colors": ["#2d4a3e", "#a8d5c2", "#f0f7f4", "#8fbc8f"], "mood": "Fresh & organic"},
        ]})
    if "campaign" in prompt_lower:
        return json.dumps({"campaign": {
            "type": "Carousel post", "bestTime": "Tue–Thu, 6–9 PM",
            "hashtags": ["#BrandMind", "#Marketing", "#Launch", "#Brand"],
            "caption": "Redefining excellence — one brand at a time. ✨",
            "ctr": "4.2%", "roi": "3.1x", "engagement": "7.8%",
            "tip": "Lead with your strongest visual. A clear CTA in the last slide drives 34% more clicks.",
            "postDays": ["Tue", "Wed", "Thu"], "targetAge": "25–34",
        }})
    if "translat" in prompt_lower:
        return json.dumps({"translations": [
            {"lang": "Spanish", "flag": "🇪🇸", "text": "Construido para lo que viene."},
            {"lang": "French",  "flag": "🇫🇷", "text": "Conçu pour demain."},
            {"lang": "German",  "flag": "🇩🇪", "text": "Gebaut für das Nächste."},
            {"lang": "Japanese","flag": "🇯🇵", "text": "未来のために構築された。"},
            {"lang": "Arabic",  "flag": "🇸🇦", "text": "مبني لما هو قادم."},
        ]})
    return "{}"
