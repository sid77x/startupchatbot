import streamlit as st
import os
from chat_engine import initialize_chat_engine
from pages import render_unified_page
from config import STARTUP_FILE

# Page config
st.set_page_config(
    page_title="Startup Chat Bot", 
    page_icon="🤖",
    layout="wide"  # Enable wide layout
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "trigger_chat" not in st.session_state:
    st.session_state.trigger_chat = None

# Check file path and initialize chat engine
if not os.path.exists(STARTUP_FILE):
    st.error(f"The file path {STARTUP_FILE} does not exist.")
    st.stop()

chat_engine = initialize_chat_engine()

# Render single unified page
render_unified_page(chat_engine)
