from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
import requests
import tempfile
import base64
import re

app = FastAPI()

# ✅ Endpoints for agent services
TRANSCRIBE_URL = "http://127.0.0.1:8004/transcribe/"
RETRIEVE_URL = "http://127.0.0.1:8002/ask/"
SUMMARIZE_URL = "http://127.0.0.1:8003/summarize/"
TTS_URL = "http://127.0.0.1:8004/speak/"  # ✅ This was missing earlier

@app.post("/talk/")
async def process_audio(file: UploadFile = File(...)):
    try:
        print("🔁 Step 1: Saving audio file...")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            temp_audio.write(await file.read())
            temp_audio_path = temp_audio.name

        print("🎤 Step 2: Transcribing...")
        with open(temp_audio_path, "rb") as f:
            transcription_response = requests.post(TRANSCRIBE_URL, files={"file": f})
        print("🧾 Whisper response:", transcription_response.text)

        query = transcription_response.json().get("transcription", "")
        if not query:
            raise Exception("Transcription failed or empty.")

        print("🧠 Step 3: Retrieving info...")
        company = re.findall(r"\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b", query)
        clean_query = company[-1] if company else query
        print("📌 Clean query:", clean_query)

        retrieval_response = requests.get(RETRIEVE_URL, params={"query": clean_query})
        print("📚 Retriever response:", retrieval_response.text)

        chunks = retrieval_response.json().get("answers", [])
        if not chunks:
            raise Exception("Retriever returned no results.")

        print("💡 Step 4: Summarizing...")
        summarize_response = requests.post(SUMMARIZE_URL, json={"answers": chunks})
        print("📄 Summary response:", summarize_response.text)

        summary = summarize_response.json().get("summary", "")
        if not summary:
            raise Exception("Summary is empty.")

        print("🔊 Step 5: Speaking...")
        speak_response = requests.post(TTS_URL, params={"text": summary})
        print("📢 TTS complete!")

        encoded_audio = base64.b64encode(speak_response.content).decode("utf-8")

        print("✅ Returning full response.")
        return {
            "query": query,
            "summary": summary,
            "spoken_response": encoded_audio
        }

    except Exception as e:
        print("❌ FULL ERROR LOG:", str(e))
        return {"error": str(e)}