from abc import ABC, abstractmethod
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from config import LLM_CONFIGS, DEFAULT_LLM


def get_llm(provider: str = DEFAULT_LLM):
    cfg = LLM_CONFIGS[provider]
    if provider == "gemini":
        return ChatGoogleGenerativeAI(model=cfg["model"], google_api_key=cfg["api_key"])
    elif provider == "groq":
        return ChatGroq(model=cfg["model"], groq_api_key=cfg["api_key"])
    elif provider == "openai":
        return ChatOpenAI(model=cfg["model"], openai_api_key=cfg["api_key"])
    raise ValueError(f"Unknown LLM provider: {provider}")


class BaseAgent(ABC):
    def __init__(self, llm_provider: str = DEFAULT_LLM):
        self.llm = get_llm(llm_provider)
        self.name = "BaseAgent"

    @abstractmethod
    def run(self, task: str, **kwargs) -> dict:
        """Execute the agent task. Returns dict with 'output', 'file_path', 'message'."""
        pass

    def think(self, prompt: str) -> str:
        """Use LLM to reason about a task."""
        response = self.llm.invoke(prompt)
        return response.content
