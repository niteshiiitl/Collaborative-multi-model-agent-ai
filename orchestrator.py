from agents.base_agent import get_llm
from agents import PDFAgent, ExcelAgent, PPTAgent, DataAgent, VideoAgent
from config import DEFAULT_LLM, AGENT_LLM_MAP


AGENT_MAP = {
    "pdf":        PDFAgent,
    "excel":      ExcelAgent,
    "powerpoint": PPTAgent,
    "ppt":        PPTAgent,
    "data":       DataAgent,
    "analysis":   DataAgent,
    "video":      VideoAgent,
}

ROUTING_PROMPT = """You are an orchestrator for a multi-agent system.
Given a user task, decide which agent(s) to use.

Available agents:
- pdf: Create PDF documents, reports, letters
- excel: Create spreadsheets, tables, data files
- powerpoint: Create presentations, slide decks
- data: Analyze data, generate charts, insights
- video: Summarize YouTube videos or local video files

User task: {task}

Respond with ONLY a comma-separated list of agent names to use (e.g., "pdf" or "data,excel").
Choose the most relevant agent(s). If multiple outputs are needed, list all."""


class Orchestrator:
    def __init__(self, llm_provider: str = DEFAULT_LLM):
        self.llm_provider = llm_provider
        self._llm = None

    @property
    def llm(self):
        if self._llm is None:
            # Orchestrator always uses Gemini for smart routing
            self._llm = get_llm(AGENT_LLM_MAP["orchestrator"])
        return self._llm

    def route(self, task: str) -> list[str]:
        prompt = ROUTING_PROMPT.format(task=task)
        response = self.llm.invoke(prompt)
        agents_raw = response.content.strip().lower()
        agents = [a.strip() for a in agents_raw.split(",") if a.strip() in AGENT_MAP]
        return agents if agents else ["pdf"]

    def run(self, task: str, **kwargs) -> list[dict]:
        selected = self.route(task)
        results = []
        for agent_key in selected:
            agent_cls = AGENT_MAP[agent_key]
            # Each agent gets its optimal LLM
            optimal_llm = AGENT_LLM_MAP.get(agent_key, self.llm_provider)
            agent = agent_cls(llm_provider=optimal_llm)
            result = agent.run(task, **kwargs)
            result["agent"] = agent.name
            result["agent_key"] = agent_key
            results.append(result)
        return results
