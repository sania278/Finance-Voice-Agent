import streamlit as st
import requests
import tempfile
import os
import base64

st.set_page_config(page_title="Finance Voice Assistant", page_icon="💬")
st.title("🎙️ Finance Voice Assistant")
st.markdown("Upload your voice query about a stock or company and get a summarized spoken response.")

audio_file = st.file_uploader("Upload an audio file (.mp3, .m4a, .wav)", type=["mp3", "m4a", "wav"])

if audio_file is not None:
    with st.spinner("⏳ Processing your audio..."):
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp:
            temp.write(audio_file.read())
            temp_path = temp.name

        # Send to orchestrator backend
        with open(temp_path, "rb") as f:
            response = requests.post("http://127.0.0.1:8005/talk/", files={"file": f})

        os.remove(temp_path)  # Cleanup

        if response.status_code == 200:
            result = response.json()

            st.success("✅ Here's your result:")

            st.subheader("📝 Transcribed Query")
            st.write(result.get("query", "Not found"))

            st.subheader("📊 Financial Summary")
            st.write(result.get("summary", "Not found"))

            st.subheader("🔊 Voice Response")

            if "spoken_response" in result:
                audio_data = base64.b64decode(result["spoken_response"])

                with open("temp_response.mp3", "wb") as f:
                    f.write(audio_data)

                st.audio("temp_response.mp3", format="audio/mp3")
            else:
                st.warning("⚠️ Voice response not received.")
        else:
            st.error("❌ Error: Could not process the audio.")
