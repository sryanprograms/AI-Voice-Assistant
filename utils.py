from openai import OpenAI
import os
from dotenv import load_dotenv
import base64
import streamlit as st
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


def get_answer(messages):
    # Access language and scenario directly from st.session_state
    language = st.session_state.get('language', 'default language')  # Provide a default value
    scenario = st.session_state.get('scenario', 'default scenario')  # Provide a default value
    level = st.session_state.get('level', 'default level')

    system_message = [{
        "role": "system",
        "content": f"""
* 		Initiate the Practice Session: Begin by setting the context in English to ease the user into the practice scenario. Example: "Okay, let's start practicing ordering food in {language}. Imagine you're in a local café. What would you like to order?"
* 		User-Led Conversation: Allow the user to initiate the conversation in the target language. Do not begin the dialogue in {language}; instead, prompt the user to make the first move.
* 		Correct Mistakes Gently: Monitor the user's pronunciation, grammar, and vocabulary. When corrections are needed, provide them gently and in English. Offer the correct form and encourage the user to try again. Example: "In {language}, to order an espresso and a croissant, you'd say: 'Olá! Gostaria de um café espresso e um croissant, por favor.' Now, let's try that again."
* 		Provide Contextual Feedback: Feedback should include the correct sentence structure, pronunciation tips, and any cultural nuances relevant to the scenario. Ensure that feedback is constructive, aimed at building the user's confidence and competence in the language.
* 		Language Proficiency Consideration: Adjust the complexity of your responses based on the user's described proficiency level, {level}. Ensure the tasks and corrections are appropriate for their skill level, challenging them sufficiently without causing frustration.

"""
    }]
    
    # Combine the system message with user messages
    combined_messages = system_message + messages
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=combined_messages
    )
    
    return response.choices[0].message.content

def speech_to_text(audio_data):
    with open(audio_data, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            response_format="text",
            file=audio_file
        )
    return transcript

def text_to_speech(input_text):
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=input_text
    )
    webm_file_path = "temp_audio_play.mp3"
    with open(webm_file_path, "wb") as f:
        response.stream_to_file(webm_file_path)
    return webm_file_path

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)
