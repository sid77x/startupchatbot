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
        .startup-messages {
            max-width: 100%;
            overflow-x: hidden;
            word-wrap: break-word;
            margin-top: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("Startup Incubators")
    
    # First display all tabs and buttons
    tabs = st.tabs(["Innovation Centre", "MUTBI", "Manipal Bio-Incubator"])
    incubator_data = [
        (INNOVATION_CENTRE_STARTUPS, "ic", "Innovation Centre Startups"),
        (MUTBI_STARTUPS, "mutbi", "MUTBI Startups"),
        (MBI_STARTUPS, "mbi", "Manipal Bio-Incubator Startups")
    ]

    clicked_startup = None

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
                        clicked_startup = startup

    # Then show response below all tabs if a startup was clicked
    if clicked_startup:
        try:
            with st.spinner("Generating response..."):
                response = chat_engine.chat(f"Tell me about {clicked_startup}")
                st.markdown('<div class="startup-messages">', unsafe_allow_html=True)
                with st.chat_message("user"):
                    st.markdown(f"Tell me about {clicked_startup}")
                with st.chat_message("assistant"):
                    st.markdown(response.response)
                st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
