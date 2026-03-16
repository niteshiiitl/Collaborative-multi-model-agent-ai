import os
from abc import ABC, abstractmethod
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from config import LLM_CONFIGS, DEFAULT_LLM


def _secret(key: str) -> str:
    """Read from Streamlit secrets at runtime, fall back to env vars."""
    try:
        import streamlit as st
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.getenv(key, "")


def get_llm(provider: str = DEFAULT_LLM):
    cfg = LLM_CONFIGS[provider]
    if provider == "gemini":
        api_key = _secret("GEMINI_API_KEY")
        return ChatGoogleGenerativeAI(model=cfg["model"], google_api_key=api_key)
    elif provider == "groq":
        api_key = _secret("GROQ_API_KEY")
        return ChatGroq(model=cfg["model"], groq_api_key=api_key)
    elif provider == "openai":
        api_key = _secret("OPENAI_API_KEY")
        return ChatOpenAI(model=cfg["model"], openai_api_key=api_key)
    raise ValueError(f"Unknown LLM provider: {provider}")


class BaseAgent(ABC):
    def __init__(self, llm_provider: str = DEFAULT_LLM):
        self.llm_provider = llm_provider
        self._llm = None  # lazy init
        self.name = "BaseAgent"

    @property
    def llm(self):
        if self._llm is None:
            self._llm = get_llm(self.llm_provider)
        return self._llm

    @abstractmethod
    def run(self, task: str, **kwargs) -> dict:
        pass

    def think(self, prompt: str) -> str:
        response = self.llm.invoke(prompt)
        return response.content
