import streamlit as st
import nest_asyncio

from io import BytesIO

from phi.assistant import Assistant
from phi.document.reader.pdf import PDFReader
from phi.llm.openai import OpenAIChat
from phi.knowledge import AssistantKnowledge
from phi.tools.duckduckgo import DuckDuckGo
from phi.embedder.openai import OpenAIEmbedder
from phi.vectordb.pgvector import PgVector2
from phi.storage.assistant.postgres import PgAssistantStorage

import openai

import ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

# Apply nest_asyncio for nested event loops, for streamlit
nest_asyncio.apply()

# Database connection URL for PostgreSQL
DB_URL = "postgresql+psycopg://ai:ai@localhost:5432/ai"

# Setup Assistant
# Use caching for resource efficiency
@st.cache_resource
def setup_assistant(api_key: str) -> Assistant: 
    llm = OpenAIChat(model="gpt-4o-mini", api_key=api_key)
    # Setup Assistant
    return Assistant(
        name="auto_rag_assistant",  
        llm=llm,  
        storage=PgAssistantStorage(table_name="auto_rag_storage", db_url=DB_URL),  
        knowledge_base=AssistantKnowledge(
            vector_db=PgVector2(
                db_url=DB_URL,  
                collection="auto_rag_docs",  
                embedder=OpenAIEmbedder(model="text-embedding-ada-002", dimensions=1536, api_key=api_key),  
            ),
            num_documents=3,  
        ),
        tools=[DuckDuckGo()],  # DuckDuckGo for web search
        instructions=[
            "Search your knowledge base first.",  
            "If not found, search the internet.",  
            "Provide clear and concise answers.",  
        ],
        show_tool_calls=True,  
        search_knowledge=True,  
        read_chat_history=True,  
        markdown=True,  
        debug_mode=True,  
    )

# Add a PDF to the knowledge base
def add_pdf(assistant: Assistant, file: BytesIO):
    reader = PDFReader()
    doc = reader.read(file)
    # If the document can be read
    if doc:
        assistant.knowledge_base.load_documents(doc, upsert=True)
        st.success("PDF added to the knowledge base.")
    else:
        st.error("Failed to read the PDF.")

# Query Assistant and return response
def query_assistant(assistant: Assistant, query: str) -> str:
    return "".join([x for x in assistant.run(query)])

# Check if OpenAI API key is valid
def check_openai_api_key(api_key: str) -> bool:
    client = openai.OpenAI(api_key=api_key)
    try:
        client.models.list()
    except openai.AuthenticationError:
        return False
    else:
        return True

# Main function, handle Streamlit UI/UX
def main():
    st.set_page_config(page_title="AutoRAG", layout="wide")
    st.title("AutoRAG: Autonomous RAG")

    api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
    if not api_key:
        st.sidebar.warning("Enter OpenAI API Key to continue.")
        st.stop()
    if not check_openai_api_key(api_key):
        st.sidebar.warning("Please enter a valid OpenAI API Key.")
        st.stop()
    
    assistant = setup_assistant(api_key)
    
    uploaded_file = st.sidebar.file_uploader("Upload PDFs", type=["pdf"])
    if uploaded_file and st.sidebar.button("Add to Knowledge Base"):
        add_pdf(assistant, BytesIO(uploaded_file.read()))
    
    query = st.text_input("Ask your questions:", placeholder="Ask ChatGPT")

    if st.button("Get answer"):
        # Check for empty questions
        if query.strip():
            with st.spinner("Thinking..."):
                response = query_assistant(assistant, query)
                st.write("**Response:**", response)
        else:
            st.error("Please enter your question.")

if __name__ == "__main__":
    main()