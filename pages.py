import streamlit as st
from config import INNOVATION_CENTRE_STARTUPS, MUTBI_STARTUPS, MBI_STARTUPS
from utils import handle_click

def render_unified_page(chat_engine):
    # Custom CSS for chat input width
    st.markdown("""
        <style>
        .stButton button {
            height: 50px;
            white-space: normal;
            text-align: center;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .custom-input-container {
            position: relative;
            height: 50px;
            width: 100%;
            max-width: 300px; /* Adjust max width */
            margin: 0 auto; /* Center align */
            padding-top: 1rem;
        }
        .custom-textarea {
            width: 100%;
            resize: none;
            padding: 10px;
            font-size: 14px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state variables
    if 'trigger_chat' not in st.session_state:
        st.session_state.trigger_chat = None
    if 'current_response' not in st.session_state:
        st.session_state.current_response = None

    startup_col, chat_col = st.columns([0.6, 0.4])

    with startup_col:
        st.title("Startup Incubators")
        
        tabs = st.tabs(["Innovation Centre", "MUTBI", "Manipal Bio-Incubator"])
        incubator_data = [
            (INNOVATION_CENTRE_STARTUPS, "ic", "Innovation Centre Startups"),
            (MUTBI_STARTUPS, "mutbi", "MUTBI Startups"),
            (MBI_STARTUPS, "mbi", "Manipal Bio-Incubator Startups")
        ]
        
        for tab, (startups, key, title) in zip(tabs, incubator_data):
            with tab:
                st.subheader(title)
                search_query = st.text_input("Search startups", key=f"{key}_search")
                filtered_startups = [s for s in startups if search_query.lower() in s.lower()] if search_query else startups
                
                if not filtered_startups:
                    st.warning("No startups found matching your search.")
                    continue
                    
                st.markdown(f"Showing {len(filtered_startups)} startups")
                
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
                if st.session_state.trigger_chat:
                    query = st.session_state.trigger_chat
                    st.session_state.trigger_chat = None
                
                    # Clear previous messages for startup section
                    st.session_state.startup_messages = [{"role": "user", "content": query}]
                
                    try:
                        with st.spinner("Generating response..."):
                            response = chat_engine.chat(query)
                            st.session_state.startup_messages.append(
                                {"role": "assistant", "content": response.response}
                            )
                    except Exception as e:
                        st.error(f"Error generating response: {str(e)}")
                
                # Display messages only for "Startup Incubators" section
                if "startup_messages" in st.session_state:
                    for message in st.session_state.startup_messages:
                        with st.chat_message(message["role"]):
                            st.markdown(message["content"])


   with chat_col:
        st.title("Chat with AI")
    
        # Input field fixed below the title
        st.markdown('<div class="custom-input-container">', unsafe_allow_html=True)
        prompt = st.text_area(
            "Type your query:",
            placeholder="What would you like to know about startups?",
            key="custom_chat_input",
            height=35
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
        if st.button("Send", key="send_button"):
            if prompt:
                # Clear chat messages for new query
                st.session_state.chat_messages = [{"role": "user", "content": prompt}]
    
                with st.chat_message("user"):
                    st.markdown(prompt)
    
                # Generate and display the assistant's response
                with st.chat_message("assistant"):
                    try:
                        with st.spinner("Generating response..."):
                            response = chat_engine.chat(prompt)
                            st.session_state.chat_messages.append(
                                {"role": "assistant", "content": response.response}
                            )
                            st.markdown(response.response)
                    except Exception as e:
                        st.error(f"Error generating response: {str(e)}")
    
        # Display chat messages only for "Chat with AI" section
        if "chat_messages" in st.session_state:
            for message in st.session_state.chat_messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
