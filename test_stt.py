import requests

file_path = r"C:\Users\Sanaiyah\finance-voice-agent\Audio samples\apple.m4a"

with open(file_path, "rb") as audio_file:
    response = requests.post("http://127.0.0.1:8004/transcribe/", files={"file": audio_file})

print("Transcription response:", response.text)
