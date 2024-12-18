import streamlit as st
import os
from chat_engine import initialize_chat_engine
from pages import render_home_page, render_startup_page, render_chat_page
from config import (STARTUP_FILE, INNOVATION_CENTRE_STARTUPS, 
                   MUTBI_STARTUPS, MBI_STARTUPS)

# Page config
st.set_page_config(page_title="Startup Chat Bot", page_icon="🤖")

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "home"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "trigger_chat" not in st.session_state:
    st.session_state.trigger_chat = None

# Check file path
if not os.path.exists(STARTUP_FILE):
    st.error(f"The file path {STARTUP_FILE} does not exist.")
    st.stop()

# Initialize chat engine
chat_engine = initialize_chat_engine()

# Add back button to all pages except home
if st.session_state.page != "home":
    if st.button("← Back to Home", key="global_back"):
        st.session_state.page = "home"
        st.session_state.messages = []

# Render appropriate page
if st.session_state.page == "home":
    render_home_page()
elif st.session_state.page == "innovation_centre":
    render_startup_page("Innovation Centre", "Description of Innovation Centre...", 
                       INNOVATION_CENTRE_STARTUPS, "ic")
elif st.session_state.page == "mutbi":
    render_startup_page("MUTBI", "Description of MUTBI...", 
                       MUTBI_STARTUPS, "mutbi")
elif st.session_state.page == "manipal_bio_incubator":
    render_startup_page("Manipal Bio-Incubator", "Description of Manipal Bio-Incubator...", 
                       MBI_STARTUPS, "mbi")
elif st.session_state.page == "chat":
    render_chat_page(chat_engine)
