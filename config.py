import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_LLM = os.getenv("DEFAULT_LLM", "gemini")

LLM_CONFIGS = {
    "gemini": {"model": "gemini-2.0-flash"},   # orchestration & routing
    "groq":   {"model": "llama3-8b-8192"},      # data analysis & video summary
    "openai": {"model": "gpt-4o-mini"},         # PDF, Excel, PowerPoint
}

# Each agent is assigned its optimal LLM
AGENT_LLM_MAP = {
    "pdf":        "openai",   # best structured document output
    "excel":      "openai",   # best JSON/tabular data generation
    "powerpoint": "openai",   # best structured slide content
    "ppt":        "openai",
    "data":       "groq",     # fast inference for analysis
    "analysis":   "groq",
    "video":      "groq",     # fast inference for summarization
    "orchestrator": "gemini", # smart routing
}
