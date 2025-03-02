# app/components/sidebar.py
import streamlit as st


def sidebar_controls() -> str:
    st.sidebar.title("NetworkSync Controls")

    # Mode selection
    mode = st.sidebar.selectbox("Select Mode", ["Chat", "Network Analysis", "Node Placement"])

    # Input mode for Chat only
    if mode == "Chat":
        input_mode = st.sidebar.radio("Input Mode", ["Text", "Voice", "File"])
        st.session_state.input_mode = input_mode

    return mode