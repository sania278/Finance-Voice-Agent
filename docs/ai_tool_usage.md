# 📄 AI Tool Usage Log

This document outlines the AI tools, models, prompts, and responses used in the Finance Voice Agent system for internship demonstration.

---

## 🎤 1. Whisper (Speech-to-Text)

- **Model**: `openai/whisper`
- **Mode**: Offline inference using `whisper` Python package
- **Purpose**: Converts spoken `.m4a` or `.wav` input to transcribed text.

### ✅ Sample Input:
Audio: `"How did Apple perform in the last quarter?"`

### 📜 Transcribed Output:
```text
How did Apple perform in the last quarter?

🔍 2. Retriever Agent (LangChain + FAISS)
Tool: langchain.vectorstores.FAISS

Backend: FAISS for fast similarity search

Purpose: Retrieve relevant financial chunks from a pre-indexed knowledge base.

✅ Sample Query:
"How did Apple perform in the last quarter?"

🔎 Retrieved Chunks:
- Apple reported Q4 revenue of $89.5B, down 1% Y/Y...
- iPhone sales declined, but services grew 16%...
- EPS exceeded expectations at $1.46...

🧠 3. Language Agent (Summarizer using LLM)
Model: google/flan-t5-base via Hugging Face

Tool: langchain.llms.HuggingFacePipeline

Purpose: Summarize the retrieved chunks into 2-3 sentences

📝 Prompt Format:

"Summarize the following content:\n<retrieved chunks>"


✅ Summarized Output:
Apple’s Q4 revenue was $89.5B with EPS at $1.46, beating expectations. Despite a dip in iPhone sales, service revenue saw strong growth.

🔊 4. Voice Agent (Text-to-Speech)
Tool: pyttsx3 (offline TTS engine)

Voice: Default Windows system voice

Output: Saves .mp3 as final_response.mp3

✅ Input:

Apple’s Q4 revenue was $89.5B with EPS at $1.46, beating expectations...

📦 Output:
final_response.mp3 generated and stored in the root folder

🔁 5. Orchestrator Pipeline
Framework: FastAPI

Route: POST /pipeline/

Purpose: Coordinates end-to-end flow: STT → Retrieval → Summarization → TTS

✅ Sample API Response:

{
  "final_response_path": "final_response.mp3",
  "summary": "Apple’s Q4 revenue was $89.5B..."
}

