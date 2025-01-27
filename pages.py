import streamlit as st
from config import INNOVATION_CENTRE_STARTUPS, MUTBI_STARTUPS, MBI_STARTUPS
from utils import handle_click
import re
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
    
    
    def parse_response(response_text):
        """
        Parse the raw response text into a list of dictionaries.
        Each dictionary contains details about one startup, including optional contact info.
        """
        startups = response_text.split("—------------------------------------------------------------------------------")
        parsed_startups = []
    
        for startup in startups:
            if not startup.strip():
                continue
            # Extract core details
            name_match = re.search(r"Startup Name:\s*(.+)", startup)
            desc_match = re.search(r"Description:\s*(.+)", startup, re.DOTALL)
            email_match = re.search(r"Email:\s*([\w\.-]+@[\w\.-]+)", startup)
            phone_match = re.search(r"Phone:\s*([\d]+)", startup)
            linkedin_match = re.search(r"Linkedin:\s*(\S+)", startup)
    
            parsed_startups.append({
                "name": name_match.group(1).strip() if name_match else "Unknown",
                "description": desc_match.group(1).strip() if desc_match else "No description available",
                "email": email_match.group(1).strip() if email_match else "Not provided",
                "phone": phone_match.group(1).strip() if phone_match else "Not provided",
                "linkedin": linkedin_match.group(1).strip() if linkedin_match else "Not provided",
            })
    
        return parsed_startups
    
    # Example usage: Assume `response.response` contains the raw text
    parsed_data = parse_response(response.response)
    
    if clicked_startup:
        try:
            with st.spinner(f"Fetching details for '{clicked_startup}'..."):
                # Find the clicked startup in the parsed data
                startup_info = next(
                    (s for s in parsed_data if s["name"].lower() == clicked_startup.lower()),
                    None,
                )
                
                if startup_info:
                    st.markdown('<div class="startup-messages">', unsafe_allow_html=True)
                    with st.chat_message("user"):
                        st.markdown(f"Tell me about {clicked_startup}")
                    with st.chat_message("assistant"):
                        st.markdown(f"""
                            <div>
                                <b>📌 Startup Name:</b> {startup_info['name']}<br>
                                <b>📝 Description:</b> {startup_info['description']}<br>
                                <b>📧 Email:</b> {startup_info['email']}<br>
                                <b>📞 Phone:</b> {startup_info['phone']}<br>
                                <b>🔗 LinkedIn:</b> {startup_info['linkedin']}<br>
                            </div>
                        """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.warning(f"No details found for {clicked_startup}")
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
