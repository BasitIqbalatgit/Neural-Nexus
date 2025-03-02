import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import asyncio
from app.components.chat import chat_interface
from app.components.sidebar import sidebar_controls
from app.components.visualizations import display_network_analysis, display_node_placement  # Fixed typo
from utils.api_handler import GeminiHandler, WeatherHandler
from utils.context_manager import ConversationManager
from utils.network_analyzer import NetworkAnalyzer
from utils.geo_processor import GeoProcessor
from config.settings import GEMINI_API_KEY, WEATHER_API_KEY

def main():
    # Title with uppercase "Neural Nexus" and smaller "NetworkSync AI Assistant"
    st.markdown(
        """
        <h1 style="font-size: 50px; font-weight: bold; text-transform: uppercase;">Neural Nexus</h1>
        <h2 style="font-size: 20px;">NetworkSync AI Assistant</h2>
        <p style="font-size: 16px;">An AI-powered tool to optimize public sector networks in underserved regions.</p>
        """,
        unsafe_allow_html=True
    )

    gemini_handler = GeminiHandler(GEMINI_API_KEY)
    weather_handler = WeatherHandler(WEATHER_API_KEY)
    network_analyzer = NetworkAnalyzer(model_path="data/models/network_predictor.pkl")
    geo_processor = GeoProcessor()
    if "conversation_manager" not in st.session_state:
        st.session_state.conversation_manager = ConversationManager()

    mode = sidebar_controls()

    if mode == "Chat":
        chat_interface(gemini_handler, weather_handler, st.session_state.conversation_manager)
    elif mode == "Network Analysis":
        display_network_analysis(network_analyzer)
    elif mode == "Node Placement":
        display_node_placement(geo_processor)

if __name__ == "__main__":
    main()
