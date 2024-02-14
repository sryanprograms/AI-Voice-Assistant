import streamlit as st
import os
from utils import get_answer, text_to_speech, autoplay_audio, speech_to_text
from audio_recorder_streamlit import audio_recorder
from streamlit_float import *

# Float feature initialization
float_init()

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! Answer the questions above so I can help your practice! When you are ready record yourself saying 'I'm ready to start.'"}
        ]
    # if "audio_initialized" not in st.session_state:
    #     st.session_state.audio_initialized = False

initialize_session_state()

st.title("Language Assistant 🤖")


st.session_state['language'] = st.selectbox('Choose the language you want to practice', ['Spanish', 'Portuguese', 'French'])
st.session_state['scenario'] = st.text_input("What scenario would you like to practice?")
st.session_state['level'] = st.selectbox('What level are you currently at in your learning?', ['Know nothing', 'Know a few words and phrases', 'Can hold a short conversation', 'Can have a coversation with some errors'])


# Create footer container for the microphone
footer_container = st.container()
with footer_container:
    audio_bytes = audio_recorder()


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if audio_bytes:
    # Write the audio bytes to a file
    with st.spinner("Transcribing..."):
        webm_file_path = "temp_audio.mp3"
        with open(webm_file_path, "wb") as f:
            f.write(audio_bytes)

        transcript = speech_to_text(webm_file_path)
        if transcript:
            st.session_state.messages.append({"role": "user", "content": transcript})
            with st.chat_message("user"):
                st.write(transcript)
            os.remove(webm_file_path)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking🤔..."):
            final_response = get_answer(st.session_state.messages)
        with st.spinner("Generating audio response..."):    
            audio_file = text_to_speech(final_response)
            autoplay_audio(audio_file)
        st.write(final_response)
        st.session_state.messages.append({"role": "assistant", "content": final_response})
        os.remove(audio_file)

# Float the footer container and provide CSS to target it with
footer_container.float("bottom: 0rem;")