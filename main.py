import streamlit as st
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
#import chromadb
import os
import openai
from llama_index.core.schema import TextNode
import nest_asyncio
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.openai import OpenAI
from llama_index.core.memory import ChatMemoryBuffer

# Set environment variable to use your bundled SQLite binary
os.environ["LD_LIBRARY_PATH"] = "./" 
# Page config
st.set_page_config(page_title="Startup Chat Bot", page_icon="🤖")
st.title("Startup Information Chat Bot")
st.markdown("Ask me anything about startups! 💬")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

@st.cache_resource
def initialize_chat_engine():
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        st.error("OPENAI_API_KEY environment variable is not set")
        st.stop()

    # Read and process the startup dataset
    with open('startup.txt', 'r', encoding='utf-8') as file:
        content = file.read()

    chunks = content.split('—------------------------------------------------------------------------------')
    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]

    nodes = [TextNode(text=chunk) for chunk in chunks]
    
    nest_asyncio.apply()
    
    # Initialize Chroma client and collection with persistent storage
    chroma_client = chromadb.Client()
    # chroma_client = chromadb.PersistentClient(path="C:/Users/gupta/OneDrive/Desktop/Ecell/startup software/chroma_db")
    chroma_collection = chroma_client.create_collection("quickstart1")
    
    # Ensure the collection is created
    if not chroma_collection:
        st.error("Failed to create Chroma collection")
        st.stop()
    
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    index = VectorStoreIndex(nodes, storage_context=storage_context)
    
    memory = ChatMemoryBuffer.from_defaults(token_limit=1500)
    chat_engine = index.as_chat_engine(
        chat_mode="context",
        system_prompt=(
            "You are a chatbot, able to have normal interactions, as well as give"
            " detailed explainations of different startups."
        ),
    )
    
    return chat_engine

# Initialize chat engine
chat_engine = initialize_chat_engine()

# Check if the file path is set
file_path = 'startup.txt'
if not os.path.exists(file_path):
    st.error(f"The file path {file_path} does not exist. Please check the path and try again.")
    st.stop()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("What would you like to know about startups?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        response = chat_engine.chat(prompt)
        st.markdown(response.response)
        st.session_state.messages.append({"role": "assistant", "content": response.response})
