import streamlit as st

def clear_chat():
    st.session_state.messages = []

def handle_click(target_page, startup_query=None):
    st.session_state.page = target_page
    if startup_query:
        st.session_state.trigger_chat = startup_query
    if target_page == "home":
        clear_chat()
