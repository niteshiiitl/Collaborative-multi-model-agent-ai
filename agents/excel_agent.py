import os
import json
import pandas as pd
from .base_agent import BaseAgent


class ExcelAgent(BaseAgent):
    def __init__(self, llm_provider="gemini"):
        super().__init__(llm_provider)
        self.name = "Excel Agent"

    def run(self, task: str, **kwargs) -> dict:
        output_path = kwargs.get("output_path", "outputs/output.xlsx")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        prompt = f"""You are a data and spreadsheet expert.
Task: {task}
Generate realistic tabular data as a JSON object with this structure:
{{
  "sheet_name": "Sheet title",
  "headers": ["col1", "col2", ...],
  "rows": [["val1", "val2", ...], ...]
}}
Return ONLY valid JSON, no explanation."""

        raw = self.think(prompt)

        # Extract JSON from response
        try:
            start = raw.find("{")
            end = raw.rfind("}") + 1
            data = json.loads(raw[start:end])
        except Exception:
            data = {
                "sheet_name": "Data",
                "headers": ["Column A", "Column B"],
                "rows": [["No data", "generated"]],
            }

        df = pd.DataFrame(data["rows"], columns=data["headers"])
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name=data.get("sheet_name", "Sheet1"), index=False)

        return {
            "output": df.to_string(),
            "file_path": output_path,
            "message": f"Excel file created at {output_path}",
        }
