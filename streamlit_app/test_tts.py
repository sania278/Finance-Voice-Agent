import requests

url = "http://127.0.0.1:8004/speak/"
params = {"text": "Your Asia tech allocation is 22 percent. TSMC beat estimates by 4 percent."}

response = requests.post(url, params=params)

# Save response audio
with open("spoken_response.mp3", "wb") as f:
    f.write(response.content)

print("Voice saved to spoken_response.mp3 ✅")
