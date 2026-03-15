import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_LLM = os.getenv("DEFAULT_LLM", "gemini")

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
