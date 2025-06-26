import streamlit as st
import requests
import base64

st.title("Finance Voice Assistant")
st.markdown("Upload your voice query about a stock or company and get a summarized spoken response.")

uploaded_file = st.file_uploader("Upload an audio file (.mp3, .m4a, .wav)", type=["mp3", "m4a", "wav"])

if uploaded_file is not None:
    st.success("Success! Here's your result:")

    files = {'file': uploaded_file}

    # Step 1: Send to orchestrator (talk API)
    response = requests.post("http://127.0.0.1:8005/talk/", files=files)

    if response.status_code == 200:
        result = response.json()
        transcription = result.get("query", "Not found")
        summary = result.get("summary", "Not found")
        audio_base64 = result.get("spoken_response", "")

        st.subheader("📝 Transcribed Query")
        st.write(transcription)

        st.subheader("📊 Financial Summary")
        st.write(summary)

        st.subheader("🔊 Voice Response")
        if audio_base64:
            st.audio(base64.b64decode(audio_base64), format="audio/mp3")
        else:
            st.warning("Voice response not available.")
    else:
        st.error("Failed to connect to backend API.")
