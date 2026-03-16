import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from orchestrator import Orchestrator

st.set_page_config(page_title="Multi-Agent System", page_icon="🤖", layout="wide")

# Debug: show what secrets are available (remove after fixing)
with st.expander("Debug: Secrets Check"):
    try:
        keys = list(st.secrets.keys())
        st.write("Secret keys found:", keys)
        gemini = st.secrets.get("GEMINI_API_KEY", "NOT FOUND")
        st.write("GEMINI_API_KEY:", "SET" if gemini and gemini != "NOT FOUND" else "MISSING")
    except Exception as e:
        st.error(f"Secrets error: {e}")

st.title("Collaborative Multi-Agent System")
st.caption("Powered by Gemini · Groq · OpenAI via LangChain")

# Sidebar config
with st.sidebar:
    st.header("⚙️ Configuration")
    llm_choice = st.selectbox("LLM Provider", ["gemini", "groq", "openai"], index=0)
    st.markdown("---")
    st.markdown("**Agents Available:**")
    st.markdown("- 📄 PDF Generator")
    st.markdown("- 📊 Excel Creator")
    st.markdown("- 📑 PowerPoint Maker")
    st.markdown("- 🔍 Data Analyst")
    st.markdown("- 🎥 Video Summarizer")
    st.markdown("---")
    st.info("The orchestrator auto-selects the right agent(s) for your task.")

# Main input
task = st.text_area(
    "Describe your task",
    placeholder="e.g. Create a sales report PDF for Q1 2024\n"
                "Summarize this YouTube video: https://youtube.com/...\n"
                "Analyze sales data and create an Excel file\n"
                "Make a PowerPoint about climate change",
    height=120,
)

# Optional inputs
col1, col2 = st.columns(2)
with col1:
    video_source = st.text_input("Video URL or path (for video tasks)", placeholder="https://youtube.com/watch?v=...")
with col2:
    csv_file = st.file_uploader("Upload CSV (for data analysis)", type=["csv"])

if st.button("🚀 Run Agents", type="primary", use_container_width=True):
    if not task.strip():
        st.warning("Please enter a task first.")
    else:
        with st.spinner("Orchestrating agents..."):
            kwargs = {}
            if video_source:
                kwargs["source"] = video_source
            if csv_file:
                import tempfile, pandas as pd
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
                tmp.write(csv_file.read())
                tmp.close()
                kwargs["csv_path"] = tmp.name

            try:
                orchestrator = Orchestrator(llm_provider=llm_choice)

                # Show routing decision
                selected_agents = orchestrator.route(task)
                st.info(f"🎯 Routing to: **{', '.join(selected_agents)}**")

                results = orchestrator.run(task, **kwargs)

                for result in results:
                    st.markdown(f"---")
                    st.subheader(f"✅ {result['agent']}")
                    st.success(result.get("message", "Done"))

                    # Show text output
                    if result.get("output"):
                        with st.expander("View Generated Content", expanded=True):
                            st.text(result["output"])

                    # Show dataframe for data agent
                    if result.get("dataframe"):
                        with st.expander("View Data Table"):
                            st.markdown(result["dataframe"], unsafe_allow_html=True)

                    # Show chart
                    if result.get("file_path") and result["file_path"] and result["file_path"].endswith(".png"):
                        st.image(result["file_path"], caption="Analysis Chart")

                    # Download button for files
                    fp = result.get("file_path")
                    if fp and os.path.exists(fp) and not fp.endswith(".png"):
                        with open(fp, "rb") as f:
                            st.download_button(
                                label=f"⬇️ Download {os.path.basename(fp)}",
                                data=f.read(),
                                file_name=os.path.basename(fp),
                                key=f"dl_{result['agent_key']}",
                            )

            except Exception as e:
                st.error(f"Error: {e}")
                st.exception(e)
