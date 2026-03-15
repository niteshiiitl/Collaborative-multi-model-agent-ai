import os
import io
import json
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from .base_agent import BaseAgent


class DataAgent(BaseAgent):
    def __init__(self, llm_provider="gemini"):
        super().__init__(llm_provider)
        self.name = "Data Analysis Agent"

    def run(self, task: str, **kwargs) -> dict:
        output_dir = kwargs.get("output_dir", "outputs")
        csv_path = kwargs.get("csv_path", None)
        os.makedirs(output_dir, exist_ok=True)

        if csv_path and os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            data_summary = df.describe().to_string()
            columns = list(df.columns)
        else:
            # Ask LLM to generate sample data
            prompt = f"""Generate sample CSV data for this analysis task: {task}
Return as JSON: {{"columns": ["col1","col2",...], "rows": [[val1,val2,...],...]}}
Make it realistic with 10 rows. Return ONLY valid JSON."""
            raw = self.think(prompt)
            try:
                start = raw.find("{")
                end = raw.rfind("}") + 1
                sample = json.loads(raw[start:end])
                df = pd.DataFrame(sample["rows"], columns=sample["columns"])
            except Exception:
                df = pd.DataFrame({"Value": [1, 2, 3, 4, 5], "Category": ["A", "B", "C", "D", "E"]})
            data_summary = df.describe().to_string()
            columns = list(df.columns)

        # LLM analysis
        analysis_prompt = f"""You are a data analyst.
Task: {task}
Data columns: {columns}
Data summary:
{data_summary}

Provide:
1. Key insights from the data
2. Trends and patterns
3. Recommendations
Be concise and actionable."""

        analysis = self.think(analysis_prompt)

        # Generate a chart
        chart_path = os.path.join(output_dir, "analysis_chart.png")
        try:
            numeric_cols = df.select_dtypes(include="number").columns
            if len(numeric_cols) >= 1:
                fig, ax = plt.subplots(figsize=(8, 4))
                df[numeric_cols[:3]].plot(ax=ax, kind="bar" if len(df) <= 15 else "line")
                ax.set_title("Data Analysis Chart")
                ax.set_xlabel("Index")
                plt.tight_layout()
                plt.savefig(chart_path)
                plt.close()
        except Exception:
            chart_path = None

        return {
            "output": analysis,
            "file_path": chart_path,
            "dataframe": df.to_html(index=False),
            "message": "Data analysis complete",
        }
