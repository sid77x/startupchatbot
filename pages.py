import streamlit as st
from config import INNOVATION_CENTRE_STARTUPS, MUTBI_STARTUPS, MBI_STARTUPS
from utils import handle_click

def render_unified_page(chat_engine):
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
            max-width: 300px;
            margin: 0 auto;
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
        .startup-messages {
            max-width: 100%;
            overflow-x: hidden;
            word-wrap: break-word;
            margin-top: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Define main columns
    startup_col, chat_col = st.columns([0.6, 0.4])

    # Startup Incubators Section
    with startup_col:
        st.title("Startup Incubators")
        
        tabs = st.tabs(["Innovation Centre", "MUTBI", "Manipal Bio-Incubator"])
        incubator_data = [
            (INNOVATION_CENTRE_STARTUPS, "ic", "Innovation Centre Startups"),
            (MUTBI_STARTUPS, "mutbi", "MUTBI Startups"),
            (MBI_STARTUPS, "mbi", "Manipal Bio-Incubator Startups")
        ]

        # Create a placeholder for startup response at the top level of startup column
        startup_response_placeholder = st.empty()

        for tab, (startups, key, title) in zip(tabs, incubator_data):
            with tab:
                st.subheader(title)
                search_query = st.text_input(f"Search {title}", key=f"{key}_search")
                filtered_startups = [s for s in startups if search_query.lower() in s.lower()] if search_query else startups
                
                if not filtered_startups:
                    st.warning("No startups found matching your search.")
                    continue
                    
                st.markdown(f"Showing {len(filtered_startups)} startups")
                cols = st.columns(3)
                
                for idx, startup in enumerate(filtered_startups):
                    with cols[idx % 3]:
                        if st.button(
                            startup,
                            key=f"{key}_startup_{idx}",
                            use_container_width=True
                        ):
                            with startup_response_placeholder:
                                try:
                                    with st.spinner("Generating response..."):
                                        response = chat_engine.chat(f"Tell me about {startup}")
                                        st.markdown('<div class="startup-messages">', unsafe_allow_html=True)
                                        with st.chat_message("user"):
                                            st.markdown(f"Tell me about {startup}")
                                        with st.chat_message("assistant"):
                                            st.markdown(response.response)
                                        st.markdown('</div>', unsafe_allow_html=True)
                                except Exception as e:
                                    st.error(f"Error generating response: {str(e)}")

    # Chat with AI Section
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

        # Create a placeholder for chat response
        chat_response_placeholder = st.empty()

        if st.button("Send", key="send_button"):
            if prompt:
                with chat_response_placeholder:
                    try:
                        with st.spinner("Generating response..."):
                            response = chat_engine.chat(prompt)
                            with st.chat_message("user"):
                                st.markdown(prompt)
                            with st.chat_message("assistant"):
                                st.markdown(response.response)
                    except Exception as e:
                        st.error(f"Error generating response: {str(e)}")
