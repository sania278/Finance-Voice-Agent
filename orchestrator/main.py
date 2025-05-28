from fastapi import FastAPI, File, UploadFile
import requests
import tempfile

app = FastAPI()

# Set endpoints for agents
TRANSCRIBE_URL = "http://127.0.0.1:8004/transcribe/"
RETRIEVE_URL = "http://127.0.0.1:8002/ask/"
SUMMARIZE_URL = "http://127.0.0.1:8003/summarize/"
TTS_URL = "http://127.0.0.1:8004/speak/"

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
        
        print("🔎 Whisper response:", transcription_response.text)
        query = transcription_response.json().get("transcription", "")

        if not query:
            raise Exception("Transcription failed or empty.")

        print("🧠 Step 3: Retrieving info...")
        retrieval_response = requests.get(RETRIEVE_URL, params={"query": query})
        print("📚 Retriever response:", retrieval_response.text)
        chunks = retrieval_response.json().get("answers", [])

        if not chunks:
            raise Exception("Retriever returned no results.")

        print("💡 Step 4: Summarizing...")
        summarize_response = requests.post(SUMMARIZE_URL, json={"answers": chunks})
        print("📄 Summary response:", summarize_response.text)
        summary = summarize_response.json().get("summary", "")

        print("🔊 Step 5: Speaking...")
        speak_response = requests.post(TTS_URL, params={"text": summary})
        print("📢 TTS complete!")

        return {
            "query": query,
            "summary": summary,
            "spoken_response": speak_response.content.decode("ISO-8859-1")
        }

    except Exception as e:
        print("❌ FULL ERROR LOG:", str(e))
        return {"error": str(e)}
