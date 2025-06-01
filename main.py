import os
import streamlit as st
from dotenv import load_dotenv
from src.utils.document_loader import DocumentLoader
from src.utils.vector_store import VectorStore
from src.utils.qa_system import QASystem

# Load environment variables
print("Current working directory:", os.getcwd())
print("Looking for .env file...")
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(f"API Key loaded: {'Yes' if OPENAI_API_KEY else 'No'}")
if not OPENAI_API_KEY:
    print("WARNING: OPENAI_API_KEY not found in environment variables")

# UI Configuration
st.set_page_config(
    page_title="Cloud Ops AI Assistant",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTextInput>div>div>input {
        font-size: 1.2rem;
    }
    .answer-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
        border: 1px solid #e0e0e0;
    }
    .source-box {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 0.5rem;
        border: 1px solid #e0e0e0;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 0.3rem;
        font-size: 1rem;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .copy-button {
        background-color: #2196F3;
        color: white;
        padding: 0.3rem 0.6rem;
        border: none;
        border-radius: 0.3rem;
        font-size: 0.9rem;
        cursor: pointer;
    }
    .copy-button:hover {
        background-color: #1976D2;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize components
@st.cache_resource
def initialize_components():
    # Load documents
    loader = DocumentLoader()
    docs = loader.load_pdfs("data")
    
    # Create vector store
    vector_store = VectorStore(OPENAI_API_KEY)
    vector_store.create_vector_store(docs)
    
    # Create QA system
    qa_system = QASystem(OPENAI_API_KEY, vector_store)
    
    return qa_system

# Sidebar
with st.sidebar:
    st.title("☁️ Cloud Ops AI")
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    This AI assistant helps you find answers to AWS and cloud operations questions using official documentation.
    
    **Features:**
    - Search across AWS documentation
    - Get detailed answers with sources
    - Copy answers to clipboard
    """)
    st.markdown("---")
    st.markdown("### Documentation")
    st.markdown("Currently loaded:")
    for file in os.listdir("data"):
        if file.endswith(".pdf"):
            st.markdown(f"- {file}")

# Header
st.title("☁️ AI Cloud Ops Assistant")
st.markdown("Ask questions about AWS, cloud operations, and best practices")

# Initialize QA system
try:
    qa_system = initialize_components()
except Exception as e:
    st.error(f"Error initializing the system: {str(e)}")
    st.info("Please make sure you have PDF documents in the 'data' directory.")
    st.stop()

# Search Interface
with st.container():
    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input(
            "Ask a cloud question",
            placeholder="e.g., 'How do I use AWS CLI?' or 'Explain EC2 instance types'",
            label_visibility="collapsed"
        )
    with col2:
        search_button = st.button("Search", use_container_width=True)

# Answer Display
if query:
    with st.spinner("Thinking..."):
        try:
            result = qa_system.answer_question(query)
            
            # Display answer with copy button
            st.markdown("### 💡 Answer")
            answer_container = st.container()
            with answer_container:
                st.markdown(f'<div class="answer-box">{result["answer"]}</div>', 
                           unsafe_allow_html=True)
                st.button("📋 Copy Answer", key="copy_answer")
            
            # Display sources
            if result["sources"]:
                st.markdown("### 📚 Sources")
                for i, source in enumerate(result["sources"], 1):
                    with st.expander(f"Source {i}"):
                        st.markdown(f'<div class="source-box">{source["content"]}</div>',
                                  unsafe_allow_html=True)
                        if "metadata" in source:
                            st.caption(f"Source: {source['metadata'].get('source', 'Unknown')}")
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit, LangChain, and OpenAI")
