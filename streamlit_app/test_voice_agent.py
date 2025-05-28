import requests

url = "http://127.0.0.1:8004/transcribe/"

# Change this to your own MP3 file path
file_path = "C:\\Users\\Sanaiyah\\Downloads\\souncheck.m4a"

with open(file_path, "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)

print("Transcription:", response.json())
