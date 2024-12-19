import streamlit as st
from config import INNOVATION_CENTRE_STARTUPS, MUTBI_STARTUPS, MBI_STARTUPS
from utils import handle_click

# Initialize session state variables
if "trigger_chat" not in st.session_state:
    st.session_state.trigger_chat = None
if "messages" not in st.session_state:
    st.session_state.messages = []

def render_unified_page(chat_engine):
    # Add CSS for consistent button sizing
    st.markdown("""
        <style>
        .stButton button {
            height: 60px;
            white-space: normal;
            text-align: center;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("Startup Incubators Chat Interface")

    # Create tabs for the main interface
    main_tabs = st.tabs(["Startups Directory", "Chat Interface"])

    # Startups Directory Tab
    with main_tabs[0]:
        # Create tabs for each incubator
        incubator_tabs = st.tabs(["Innovation Centre", "MUTBI", "Manipal Bio-Incubator"])
        incubator_data = [
            (INNOVATION_CENTRE_STARTUPS, "ic", "Innovation Centre Startups"),
            (MUTBI_STARTUPS, "mutbi", "MUTBI Startups"),
            (MBI_STARTUPS, "mbi", "Manipal Bio-Incubator Startups")
        ]
        
        for tab, (startups, key, title) in zip(incubator_tabs, incubator_data):
            with tab:
                st.subheader(title)
                
                # Search and display startups
                search_query = st.text_input("Search startups", key=f"{key}_search")
                filtered_startups = [s for s in startups if search_query.lower() in s.lower()] if search_query else startups
                
                if not filtered_startups:
                    st.warning("No startups found matching your search.")
                    continue
                    
                st.markdown(f"Showing {len(filtered_startups)} startups")
                
                # Create grid layout for startup buttons
                cols = st.columns(3)
                for idx, startup in enumerate(filtered_startups):
                    with cols[idx % 3]:
                        st.button(
                            startup,
                            key=f"{key}_startup_{idx}",
                            on_click=handle_click,
                            args=("chat", f"Tell me about {startup}"),
                            use_container_width=True
                        )

    # Chat Interface Tab
    with main_tabs[1]:
        st.subheader("Chat with AI")
        
        # Handle triggered chat queries
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

        # Chat input - Now correctly placed at the root level of the chat tab
        prompt = st.chat_input("What would you like to know about startups?")
        if prompt:
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
