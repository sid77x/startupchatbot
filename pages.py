import streamlit as st
from config import INNOVATION_CENTRE_STARTUPS, MUTBI_STARTUPS, MBI_STARTUPS
from utils import handle_click
# Method 1: Using Custom CSS for Fixed Position
def render_unified_page(chat_engine):
    # Enhanced CSS with chat input positioning
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
        .stChatInput {
            position: fixed;
            right: 0;
            width: 33% !important;
            bottom: 0;
            padding: 1rem;
            background: white;
            border-top: 1px solid #ddd;
        }
        [data-testid="column"] {
            padding-bottom: 60px;
        }
        </style>
    """, unsafe_allow_html=True)

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

    with chat_col:
        st.title("Chat with AI")
        
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

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chat input outside columns but styled with CSS
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

# Method 2: Using Empty Space for Visual Balance
def render_unified_page_spacer_method(chat_engine):
    # Basic CSS
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

    startup_col, chat_col = st.columns([0.6, 0.4])

    with startup_col:
        # Same startup column code as above...
        pass

    with chat_col:
        st.title("Chat with AI")
        
        # Same chat display code as above...
        pass

    # Create balanced columns for chat input
    left_spacer, chat_input_container, right_spacer = st.columns([0.6, 0.4, 0.2])
    with chat_input_container:
        prompt = st.chat_input("What would you like to know about startups?")
        if prompt:
            # Same prompt handling code as above...
            pass

# Method 3: Using Container with Custom Width
def render_unified_page_container_method(chat_engine):
    # Basic CSS
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

    startup_col, chat_col = st.columns([0.6, 0.4])

    with startup_col:
        # Same startup column code as above...
        pass

    with chat_col:
        st.title("Chat with AI")
        
        # Same chat display code as above...
        pass

    # Create a container and set its width
    container = st.container()
    col1, col2, _ = st.columns([0.6, 0.4, 0.2])
    with col2:
        prompt = st.chat_input("What would you like to know about startups?")
        if prompt:
            # Same prompt handling code as above...
            pass
