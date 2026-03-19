import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_LLM = os.getenv("DEFAULT_LLM", "gemini")

LLM_CONFIGS = {
    "gemini": {"model": "gemini-2.0-flash"},
    "groq":   {"model": "llama3-8b-8192"},
    "openai": {"model": "gpt-4o-mini"},
}
