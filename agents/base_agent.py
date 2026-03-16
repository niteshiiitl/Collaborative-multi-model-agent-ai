import os
from abc import ABC, abstractmethod
from config import DEFAULT_LLM


def _load_secrets():
    """Push Streamlit secrets into os.environ so LangChain picks them up automatically."""
    try:
        import streamlit as st
        for key in ["GEMINI_API_KEY", "GROQ_API_KEY", "OPENAI_API_KEY", "GOOGLE_API_KEY"]:
            if key in st.secrets and not os.environ.get(key):
                os.environ[key] = st.secrets[key]
        # LangChain Google also checks GOOGLE_API_KEY
        if "GEMINI_API_KEY" in st.secrets and not os.environ.get("GOOGLE_API_KEY"):
            os.environ["GOOGLE_API_KEY"] = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass


def get_llm(provider: str = DEFAULT_LLM):
    _load_secrets()  # ensure env vars are set before LangChain reads them

    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_groq import ChatGroq
    from langchain_openai import ChatOpenAI
    from config import LLM_CONFIGS

    cfg = LLM_CONFIGS[provider]
    if provider == "gemini":
        return ChatGoogleGenerativeAI(model=cfg["model"])
    elif provider == "groq":
        return ChatGroq(model=cfg["model"])
    elif provider == "openai":
        return ChatOpenAI(model=cfg["model"])
    raise ValueError(f"Unknown LLM provider: {provider}")


class BaseAgent(ABC):
    def __init__(self, llm_provider: str = DEFAULT_LLM):
        self.llm_provider = llm_provider
        self._llm = None
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
        return self.llm.invoke(prompt).content
