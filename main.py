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
        storage=PgAssistantStorage(table_name="auto_rag_storage", db_url=DB_URL)
        knowledge_base=AssistantKnowledge(
            vector_db=PgVector2(
                db_url=DB_URL,
                collection="auto_rag_docs",
                embedder=OpenAIEmbedder(model="text-embedding-ada-002", dimensions=1536, api_key=api_key),
            ),
            num_documents=3,
        ),
        # DuckDuckGo for web search
        tools=[DuckDuckGo()],
        instructions=[
            "First, search your knowledge base.",
            "Then, if not found search the internet.",
            "Finally, provide clear and concise answers.",
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

# Main function, handle Streamlit UI/UX
def main():
    st.set_page_config(page_title="AutoRAG", layout="wide")
    st.title("AutoRAG: Autonomous RAG")
