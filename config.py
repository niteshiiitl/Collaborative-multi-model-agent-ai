import os
from dotenv import load_dotenv

load_dotenv()

def _get(key, default=None):
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.getenv(key, default)

GEMINI_API_KEY = _get("GEMINI_API_KEY")
GROQ_API_KEY = _get("GROQ_API_KEY")
OPENAI_API_KEY = _get("OPENAI_API_KEY")
DEFAULT_LLM = _get("DEFAULT_LLM", "gemini")

LLM_CONFIGS = {
    "gemini": {
        "model": "gemini-1.5-flash",
        "api_key": GEMINI_API_KEY,
    },
    "groq": {
        "model": "llama3-8b-8192",
        "api_key": GROQ_API_KEY,
    },
    "openai": {
        "model": "gpt-4o-mini",
        "api_key": OPENAI_API_KEY,
    },
}
