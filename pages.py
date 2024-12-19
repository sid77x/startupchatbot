import streamlit as st
from config import INNOVATION_CENTRE_STARTUPS, MUTBI_STARTUPS, MBI_STARTUPS
from utils import handle_click

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

    # Create main columns for layout
    startup_col, chat_col = st.columns([0.6, 0.4])

    with startup_col:
        st.title("Startup Incubators")
        
        # Create tabs for each incubator
        tabs = st.tabs(["Innovation Centre", "MUTBI", "Manipal Bio-Incubator"])
        incubator_data = [
            (INNOVATION_CENTRE_STARTUPS, "ic", "Innovation Centre Startups"),
            (MUTBI_STARTUPS, "mutbi", "MUTBI Startups"),
            (MBI_STARTUPS, "mbi", "Manipal Bio-Incubator Startups")
        ]
        
        for tab, (startups, key, title) in zip(tabs, incubator_data):
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

    with chat_col:
        st.title("Chat with AI")
        
        # Handle chat functionality
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
