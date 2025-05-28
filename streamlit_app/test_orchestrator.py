import requests

# Endpoint for orchestrator
url = "http://127.0.0.1:8005/talk/"

# Path to your audio file (must be .mp3)
file_path = "C:\\Users\\Sanaiyah\\Downloads\\souncheck.m4a"  # replace with your own file

# Upload the voice input
with open(file_path, "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)

# Check response
if response.status_code == 200:
    result = response.json()
    print("🎤 Transcription:", result.get("query", "❌ query missing"))
    print("🧠 Summary:", result.get("summary", "❌ summary missing"))

    print("🪵 Full Response:", result)


    with open("final_response.mp3", "wb") as audio_file:
        audio_file.write(response.content)
    print("🔊 Voice response saved to final_response.mp3")
else:
    print("❌ Error:")
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

