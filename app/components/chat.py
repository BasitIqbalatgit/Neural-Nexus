# app/components/chat.py
import streamlit as st
import asyncio
import os
import tempfile
import speech_recognition as sr
from utils.api_handler import GeminiHandler, WeatherHandler
from utils.context_manager import ConversationManager
from config.settings import ALLOWED_FILE_TYPES

async def process_message(user_input: str, file_path: str, gemini_handler: GeminiHandler,
                        weather_handler: WeatherHandler, conversation_manager: ConversationManager) -> str:
    context = conversation_manager.get_context()
    if "weather" in user_input.lower():
        return weather_handler.get_weather_info(user_input)
    else:
        return await gemini_handler.generate_response(user_input, file_path, context)

def handle_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak now.")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=5, phrase_time_limit=15)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio.get_wav_data())
            text = r.recognize_google(audio)
            return text, tmp_file.name
    return None, None

def chat_interface(gemini_handler: GeminiHandler, weather_handler: WeatherHandler,
                  conversation_manager: ConversationManager):
    # Display chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input mode selection from sidebar determines behavior
    input_mode = st.session_state.input_mode
    user_input, file_path = None, None

    if input_mode == "Text":
        user_input = st.chat_input("Ask about network optimization...")
    elif input_mode == "Voice":
        if st.button("Start Voice Input"):
            user_input, file_path = handle_voice_input()
    else:  # File
        uploaded_file = st.file_uploader("Upload a file", type=ALLOWED_FILE_TYPES)
        if uploaded_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                file_path = tmp_file.name
            user_input = "Please analyze this file and provide insights."

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
            if file_path and file_path.lower().endswith(('png', 'jpg', 'jpeg')):
                st.image(file_path)

        with st.spinner("Processing..."):
            response = asyncio.run(process_message(user_input, file_path, gemini_handler,
                                                  weather_handler, conversation_manager))
            conversation_manager.add_to_context(user_input, response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)

        # Cleanup
        if file_path and os.path.exists(file_path):
            os.unlink(file_path)