import streamlit as st
from config import INNOVATION_CENTRE_STARTUPS, MUTBI_STARTUPS, MBI_STARTUPS
from utils import handle_click

def render_home_page():
    st.title("Startup Incubators")
    st.markdown("Select an incubator to learn more about its startups")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("Innovation Centre", key="home_ic_btn", 
                 on_click=handle_click, args=("innovation_centre",), use_container_width=True)
    with col2:
        st.button("MUTBI", key="home_mutbi_btn", 
                 on_click=handle_click, args=("mutbi",), use_container_width=True)
    with col3:
        st.button("Manipal Bio-Incubator", key="home_mbi_btn", 
                 on_click=handle_click, args=("manipal_bio_incubator",), use_container_width=True)

def render_startup_page(title, description, startups, page_key):
    st.title(title)
    st.markdown(description)
    
    st.button("← Back to Home", key=f"{page_key}_back_btn", 
             on_click=handle_click, args=("home",))

    col1, col2, col3 = st.columns(3)
    for idx, startup in enumerate(startups):
        with [col1, col2, col3][idx % 3]:
            st.button(startup, key=f"{page_key}_startup_{idx}", 
                     on_click=handle_click, args=("chat", f"Tell me about {startup}"), 
                     use_container_width=True)

def render_chat_page(chat_engine):
    st.title("Startup Information Chat Bot")
    st.markdown("Ask me anything about startups! 💬")

    # Handle triggered chat query
    if st.session_state.trigger_chat:
        query = st.session_state.trigger_chat
        st.session_state.trigger_chat = None
        
        st.session_state.messages.append({"role": "user", "content": query})
        try:
            with st.spinner("Generating response..."):
                response = chat_engine.chat(query)
                st.session_state.messages.append({"role": "assistant", "content": response.response})
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle user input
    if prompt := st.chat_input("What would you like to know about startups?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                with st.spinner("Generating response..."):
                    response = chat_engine.chat(prompt)
                    st.markdown(response.response)
                    st.session_state.messages.append({"role": "assistant", "content": response.response})
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")
