from fastapi import FastAPI, File, UploadFile
import whisper
import os
import tempfile

app = FastAPI()

# Load whisper model
model = whisper.load_model("base")

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            temp_audio.write(await file.read())
            temp_audio_path = temp_audio.name

        # Transcribe
        result = model.transcribe(temp_audio_path)
        os.remove(temp_audio_path)  # Clean up
        return {"transcription": result["text"]}
    except Exception as e:
        return {"error": str(e)}


import pyttsx3
from fastapi.responses import FileResponse

@app.post("/speak/")
def speak_text(text: str):
    engine = pyttsx3.init()
    output_path = "response_audio.mp3"

    # Save spoken output to file
    engine.save_to_file(text, output_path)
    engine.runAndWait()

    return FileResponse(path=output_path, filename="response_audio.mp3", media_type='audio/mpeg')
