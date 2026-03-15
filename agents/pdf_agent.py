import os
from fpdf import FPDF
from .base_agent import BaseAgent


class PDFAgent(BaseAgent):
    def __init__(self, llm_provider="gemini"):
        super().__init__(llm_provider)
        self.name = "PDF Agent"

    def run(self, task: str, **kwargs) -> dict:
        output_path = kwargs.get("output_path", "outputs/output.pdf")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Use LLM to generate content
        prompt = f"""You are a professional document writer.
Task: {task}
Generate well-structured content for a PDF document.
Use clear sections with headings marked as [HEADING] and body text.
Keep it professional and concise."""

        content = self.think(prompt)

        # Build PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        for line in content.split("\n"):
            line = line.strip()
            if not line:
                pdf.ln(4)
            elif line.startswith("[HEADING]"):
                pdf.set_font("Helvetica", "B", 14)
                pdf.multi_cell(0, 8, line.replace("[HEADING]", "").strip())
                pdf.ln(2)
            else:
                pdf.set_font("Helvetica", "", 11)
                pdf.multi_cell(0, 6, line)

        pdf.output(output_path)
        return {
            "output": content,
            "file_path": output_path,
            "message": f"PDF created at {output_path}",
        }
