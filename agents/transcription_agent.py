# agents/transcription_agent.py

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
import whisper
from gtts import gTTS
import tempfile
import os

app = FastAPI()

# Load Whisper model once
model = whisper.load_model("base")

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Transcribes uploaded audio file using OpenAI Whisper.
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            temp_audio.write(await file.read())
            temp_audio_path = temp_audio.name

        result = model.transcribe(temp_audio_path)
        os.remove(temp_audio_path)
        return {"transcription": result["text"]}
    
    except Exception as e:
        return {"error": str(e)}

@app.post("/speak/")
async def text_to_speech(text: str = Form(...)):
    """
    Converts input text to speech and streams mp3 response.
    """
    try:
        tts = gTTS(text)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tts.save(tmp.name)
            return StreamingResponse(open(tmp.name, "rb"), media_type="audio/mpeg")
    
    except Exception as e:
        return {"error": str(e)}
