# app/components/chat.py
import streamlit as st
import os
import tempfile
import speech_recognition as sr
from utils.network_analyzer import NetworkAnalyzer
from utils.api_handler import WeatherHandler
from utils.context_manager import ConversationManager
from config.settings import ALLOWED_FILE_TYPES
import pandas as pd

def process_message(user_input: str, file_path: str, network_analyzer: NetworkAnalyzer,
                   weather_handler: WeatherHandler, conversation_manager: ConversationManager) -> str:
    try:
        if "weather" in user_input.lower():
            return weather_handler.get_weather_info(user_input)
        elif file_path and file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
            predictions = network_analyzer.predict_downtime(df[['bandwidth', 'latency', 'signal_strength']])
            energy_metrics = network_analyzer.analyze_energy_efficiency(df)
            return f"Network Analysis Results:\nPredicted Uptime: {predictions[0]:.2f}%\n" \
                   f"Average Energy Usage: {energy_metrics['avg_energy_usage']:.2f}\n" \
                   f"Total Energy Usage: {energy_metrics['total_energy_usage']:.2f}"
        else:
            return "Please provide network data in CSV format for analysis."
    except Exception as e:
        return f"Error processing request: {str(e)}"

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

def chat_interface(network_analyzer: NetworkAnalyzer, weather_handler: WeatherHandler,
                  conversation_manager: ConversationManager):
    # Display chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input mode selection
    input_mode = st.session_state.get('input_mode', 'Text')
    user_input, file_path = None, None

    if input_mode == "Text":
        user_input = st.chat_input("Ask about network optimization...")
    elif input_mode == "Voice":
        if st.button("Start Voice Input"):
            user_input, file_path = handle_voice_input()
    else:  # File
        uploaded_file = st.file_uploader("Upload a CSV file", type=['csv'])
        if uploaded_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                file_path = tmp_file.name
            user_input = "Please analyze this network data."

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.spinner("Processing..."):
            response = process_message(user_input, file_path, network_analyzer,
                                    weather_handler, conversation_manager)
            conversation_manager.add_to_context(user_input, response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)

        # Cleanup
        if file_path and os.path.exists(file_path):
            os.unlink(file_path)