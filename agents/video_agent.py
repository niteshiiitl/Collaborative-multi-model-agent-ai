import os
import re
from .base_agent import BaseAgent


class VideoAgent(BaseAgent):
    def __init__(self, llm_provider="gemini"):
        super().__init__(llm_provider)
        self.name = "Video Summary Agent"

    def _is_youtube_url(self, source: str) -> bool:
        return "youtube.com" in source or "youtu.be" in source

    def _get_youtube_transcript(self, url: str) -> str:
        from youtube_transcript_api import YouTubeTranscriptApi
        video_id = None
        patterns = [r"v=([^&]+)", r"youtu\.be/([^?]+)"]
        for p in patterns:
            m = re.search(p, url)
            if m:
                video_id = m.group(1)
                break
        if not video_id:
            raise ValueError("Could not extract YouTube video ID")
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([t["text"] for t in transcript])

    def _transcribe_local_video(self, video_path: str) -> str:
        import whisper
        model = whisper.load_model("base")
        result = model.transcribe(video_path)
        return result["text"]

    def run(self, task: str, **kwargs) -> dict:
        source = kwargs.get("source", "")
        output_path = kwargs.get("output_path", "outputs/video_summary.txt")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        transcript = ""
        if source:
            try:
                if self._is_youtube_url(source):
                    transcript = self._get_youtube_transcript(source)
                elif os.path.exists(source):
                    transcript = self._transcribe_local_video(source)
            except Exception as e:
                transcript = f"[Could not extract transcript: {e}]"

        prompt = f"""You are a video content summarizer.
Task: {task}
{"Transcript: " + transcript[:4000] if transcript else "No transcript available - generate a sample summary structure."}

Provide:
1. Executive Summary (2-3 sentences)
2. Key Topics Covered
3. Main Takeaways (bullet points)
4. Notable Quotes or Moments (if any)
Keep it clear and structured."""

        summary = self.think(prompt)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(summary)

        return {
            "output": summary,
            "file_path": output_path,
            "message": f"Video summary saved to {output_path}",
        }
