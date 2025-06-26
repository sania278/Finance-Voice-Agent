
# 🎙️ Finance Voice Agent

A voice-enabled financial assistant that transcribes spoken queries, retrieves relevant market data using RAG (retrieval-augmented generation), summarizes with an LLM, and replies using speech synthesis.

Built using modular microservices in FastAPI and orchestrated via REST calls.

---

## 🧠 Features

- 🎤 **Speech-to-Text (Whisper)**: Converts voice input to text
- 🔍 **Retriever Agent (FAISS + LangChain)**: Fetches relevant financial chunks
- 🧠 **Language Agent (HuggingFace LLM)**: Summarizes retrieved info
- 🔊 **Text-to-Speech Agent (pyttsx3)**: Delivers spoken response
- 🔁 **Orchestrator**: Connects all agents into a voice pipeline

---

## 📁 Project Structure

finance-voice-agent/
├── agents/
│ ├── api_agent.py
│ ├── retriever_agent.py
│ ├── language_agent.py
│ ├── voice_agent.py
│ └── scraping_agent.py
├── orchestrator/
│ └── main.py
├── streamlit_app/
│ ├── test_language_agent.py
│ ├── test_tts.py
│ └── test_orchestrator.py
├── docs/
│ └── ai_tool_usage.md
├── requirements.txt
└── README.md


---

## 🚀 Quick Start

1. Clone and Setup Environment
```bash
git clone https://github.com/sania278/Finance-Voice-Agent.git
cd finance-voice-agent
python -m venv venv
venv\Scripts\activate   # On Windows
pip install -r requirements.txt

2. Run Microservices (in separate terminals)

uvicorn agents.api_agent:app --port 8000
uvicorn agents.retriever_agent:app --port 8002
uvicorn agents.language_agent:app --port 8003
uvicorn agents.voice_agent:app --port 8004
uvicorn orchestrator.main:app --port 8005

3. Test the System End-to-End

python streamlit_app/test_orchestrator.py


🧪 Tech Stack
Component	    Technology
STT	            OpenAI Whisper
Retriever	    FAISS + LangChain
Summarizer	    HuggingFace Flan-T5
TTS     	    pyttsx3 (offline)
API	            FastAPI + Uvicorn
Orchestration	REST microservices

📊 Example Voice Query Flow
🎙️ Input: “How did TSMC perform this quarter?”
📝 Whisper: How did TSMC perform this quarter?
🔍 FAISS: Fetched top-3 results from vector DB
🤖 Flan-T5: “TSMC beat analyst expectations by 4%. Asia tech is up 3.2%.”
🔊 pyttsx3: Output audio saved as final_response.mp3

📄 Documentation
See docs/ai_tool_usage.md for:

Model parameters

Prompt logs

Intermediate outputs

Voice-to-text and TTS traces

