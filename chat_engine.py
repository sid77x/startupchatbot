import streamlit as st
import pysqlite3
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import chromadb
import os
import openai
from llama_index.core.schema import TextNode
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.memory import ChatMemoryBuffer
import nest_asyncio
from config import STARTUP_FILE, DB_DIR, CHAT_SYSTEM_PROMPT

@st.cache_resource
def initialize_chat_engine():
    try:
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        if not openai.api_key:
            st.error("OPENAI_API_KEY environment variable is not set")
            st.stop()

        with open(STARTUP_FILE, 'r', encoding='utf-8') as file:
            content = file.read()
        
        chunks = content.split('—------------------------------------------------------------------------------')
        nodes = [TextNode(text=chunk.strip()) for chunk in chunks if chunk.strip()]
        
        nest_asyncio.apply()
        
        os.makedirs(DB_DIR, exist_ok=True)
        chroma_client = chromadb.PersistentClient(path=DB_DIR)
        
        try:
            chroma_collection = chroma_client.get_collection("quickstart2")
        except:
            chroma_collection = chroma_client.create_collection("quickstart2")
        
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        
        index = VectorStoreIndex(nodes, storage_context=storage_context)
        memory = ChatMemoryBuffer.from_defaults(token_limit=500)
        
        chat_engine = index.as_chat_engine(
            chat_mode="context",
            system_prompt=CHAT_SYSTEM_PROMPT,
        )
        
        return chat_engine
    except Exception as e:
        st.error(f"Error initializing chat engine: {str(e)}")
        st.stop()
