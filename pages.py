import streamlit as st
from config import INNOVATION_CENTRE_STARTUPS, MUTBI_STARTUPS, MBI_STARTUPS
from utils import handle_click

def render_unified_page(chat_engine):
    # Define a custom style for buttons and layout
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
    
    # Define incubator data to avoid repetition
    incubator_data = [
        (INNOVATION_CENTRE_STARTUPS, "ic", "Innovation Centre Startups"),
        (MUTBI_STARTUPS, "mutbi", "MUTBI Startups"),
        (MBI_STARTUPS, "mbi", "Manipal Bio-Incubator Startups")
    ]

    # Display tabs for each incubator
    tabs = st.tabs([data[2] for data in incubator_data])
    clicked_startup = None  # Initialize clicked startup

    # Iterate through tabs and display their content
    for tab, (startups, key, title) in zip(tabs, incubator_data):
        with tab:
            st.subheader(title)
            # Add a search bar for filtering startups
            search_query = st.text_input(f"Search {title}", key=f"{key}_search")
            filtered_startups = [
                s for s in startups if search_query.lower() in s.lower()
            ] if search_query else startups

            if not filtered_startups:
                st.warning(f"No startups found matching your search for '{search_query}'.")
                continue
            
            # Show the filtered startup count and organize buttons in columns
            st.markdown(f"**Showing {len(filtered_startups)} startups:**")
            cols = st.columns(3)  # Divide into 3 columns for better layout
            
            # Generate buttons for each startup
            for idx, startup in enumerate(filtered_startups):
                with cols[idx % 3]:  # Distribute buttons across columns
                    if st.button(
                        startup,
                        key=f"{key}_startup_{idx}",
                        use_container_width=True
                    ):
                        clicked_startup = startup

    # Generate response for the selected startup
    if clicked_startup:
        try:
            with st.spinner(f"Fetching details for '{clicked_startup}'..."):
                response = chat_engine.chat(f"Tell me about {clicked_startup}")
                # Display user query and assistant's response
                st.markdown('<div class="startup-messages">', unsafe_allow_html=True)
                with st.chat_message("user"):
                    st.markdown(f"Tell me about {clicked_startup}")
                with st.chat_message("assistant"):
                    st.markdown(response.response)
                st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
