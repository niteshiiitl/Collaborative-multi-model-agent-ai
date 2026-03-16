# Collaborative Multi-Agent System

A multi-agent AI system that automates document creation, data analysis, and video summarization through a simple web interface. Built with LangChain and Streamlit, it supports multiple LLM backends including Gemini, Groq, and OpenAI.

---

## Features

- PDF generation from natural language prompts
- Excel spreadsheet creation with structured data
- PowerPoint presentation generation
- Data analysis with charts and insights
- Video summarization from YouTube URLs or local video files
- Intelligent task routing via an LLM-powered orchestrator
- Support for multi-agent collaboration on complex tasks

---

## Project Structure

```
multi-agent-system/
├── main.py               # CLI entry point
├── orchestrator.py       # Routes tasks to the appropriate agents
├── config.py             # API key and LLM configuration
├── requirements.txt
├── .env.example          # Template for local environment variables
├── agents/
│   ├── base_agent.py     # Base class and LLM loader
│   ├── pdf_agent.py
│   ├── excel_agent.py
│   ├── ppt_agent.py
│   ├── data_agent.py
│   └── video_agent.py
└── ui/
    └── app.py            # Streamlit web interface
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/niteshiitl/Collaborative-multi-agent-system-.git
cd Collaborative-multi-agent-system-
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API keys

Copy the example env file and fill in your keys:

```bash
cp .env.example .env
```

```
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key
DEFAULT_LLM=gemini
```

### 4. Run the Streamlit app

```bash
streamlit run ui/app.py
```

---

## CLI Usage

```bash
python main.py "Create a business report about renewable energy" --llm gemini
python main.py "Summarize this video" --source https://youtube.com/watch?v=xxx
python main.py "Analyze and visualize sales data" --csv data.csv --llm groq
```

---

## Supported LLM Providers

| Provider | Models Used         |
|----------|---------------------|
| Gemini   | gemini-1.5-flash    |
| Groq     | llama3-8b-8192      |
| OpenAI   | gpt-4o-mini         |

---

## Deploying on Streamlit Cloud

This project is ready for Streamlit Cloud deployment. Instead of using a `.env` file in production, add your API keys through the Streamlit Cloud dashboard under App Settings > Secrets:

```toml
GEMINI_API_KEY = "your_key"
GROQ_API_KEY = "your_key"
OPENAI_API_KEY = "your_key"
DEFAULT_LLM = "gemini"
```

Never commit your `.env` file. It is already excluded via `.gitignore`.

---

## Requirements

- Python 3.9 or higher
- ffmpeg (required for local video transcription via Whisper)

---

## License

MIT
