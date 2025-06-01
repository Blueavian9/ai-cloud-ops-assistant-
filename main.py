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

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "processing" not in st.session_state:
    st.session_state.processing = False
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# UI Configuration
st.set_page_config(
    page_title="Cloud Ops AI Assistant",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with cool features
st.markdown("""
    <style>
    /* Global styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container with gradient background */
    .main {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
        background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
        min-height: 100vh;
    }
    
    /* Animated header */
    .header {
        background: linear-gradient(90deg, #4CAF50, #2196F3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 3s ease infinite;
        background-size: 200% 200%;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Search container with glassmorphism */
    .search-container {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease;
    }
    
    .search-container:hover {
        transform: translateY(-2px);
    }
    
    /* Enhanced input styling */
    .stTextInput>div>div>input {
        font-size: 1.2rem;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.9);
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #4CAF50;
        box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.2);
        transform: scale(1.01);
    }
    
    /* Answer container with glassmorphism */
    .answer-container {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin-top: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        animation: fadeIn 0.5s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Answer box with gradient border */
    .answer-box {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 2px solid transparent;
        background-image: linear-gradient(white, white), 
                         linear-gradient(90deg, #4CAF50, #2196F3);
        background-origin: border-box;
        background-clip: padding-box, border-box;
        margin-top: 1rem;
    }
    
    /* Source box with hover effect */
    .source-box {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 0.5rem;
        border: 1px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    
    .source-box:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Enhanced button styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #4CAF50, #45a049);
        color: white;
        padding: 0.8rem 1.5rem;
        border: none;
        border-radius: 0.5rem;
        font-size: 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    /* Chat message styling with animations */
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
        animation: slideIn 0.3s ease-out;
        position: relative;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .chat-message.user {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        margin-left: 20%;
        border-left: 4px solid #2196F3;
    }
    
    .chat-message.assistant {
        background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
        margin-right: 20%;
        border-left: 4px solid #4CAF50;
    }
    
    .chat-message .content {
        margin-bottom: 0.5rem;
    }
    
    .chat-message .timestamp {
        font-size: 0.8rem;
        color: #666;
        text-align: right;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
        padding: 1rem;
    }
    
    /* Theme toggle button */
    .theme-toggle {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 1000;
    }
    
    /* Loading animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(76, 175, 80, 0.3);
        border-radius: 50%;
        border-top-color: #4CAF50;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #666;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize components
@st.cache_resource
def initialize_components():
    if not OPENAI_API_KEY:
        raise ValueError("OpenAI API key not found. Please set it in your .env file.")
    
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
    st.markdown('<h1 class="header">☁️ Cloud Ops AI</h1>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    This AI assistant helps you find answers to AWS and cloud operations questions using official documentation.
    
    **Features:**
    - Search across AWS documentation
    - Get detailed answers with sources
    - Copy answers to clipboard
    - Chat history
    - Interactive UI
    """)
    st.markdown("---")
    st.markdown("### Documentation")
    st.markdown("Currently loaded:")
    for file in os.listdir("data"):
        if file.endswith(".pdf"):
            st.markdown(f"- {file}")
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# Main content
st.markdown('<h1 class="header">☁️ AI Cloud Ops Assistant</h1>', unsafe_allow_html=True)
st.markdown("Ask questions about AWS, cloud operations, and best practices")

# Initialize QA system
try:
    qa_system = initialize_components()
except Exception as e:
    st.error(f"Error initializing the system: {str(e)}")
    if "OpenAI API key not found" in str(e):
        st.info("Please create a .env file with your OPENAI_API_KEY")
    else:
        st.info("Please make sure you have PDF documents in the 'data' directory.")
    st.stop()

# Search Interface
with st.container():
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_input(
            "Ask a cloud question",
            placeholder="e.g., 'How do I use AWS CLI?' or 'Explain EC2 instance types'",
            label_visibility="collapsed"
        )
    with col2:
        search_button = st.button("🔍 Search", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Display chat history
if st.session_state.chat_history:
    st.markdown("### 💬 Chat History")
    for message in st.session_state.chat_history:
        with st.container():
            st.markdown(f"""
                <div class="chat-message {message['role']}">
                    <div class="content">{message['content']}</div>
                    <div class="timestamp">{message['timestamp']}</div>
                </div>
            """, unsafe_allow_html=True)

# Answer Display
if query and search_button:
    st.session_state.processing = True
    with st.spinner(""):
        st.markdown('<div class="loading"></div>', unsafe_allow_html=True)
        try:
            result = qa_system.answer_question(query)
            
            # Add to chat history
            from datetime import datetime
            st.session_state.chat_history.append({
                "role": "user",
                "content": query,
                "timestamp": datetime.now().strftime("%H:%M")
            })
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": result["answer"],
                "timestamp": datetime.now().strftime("%H:%M")
            })
            
            # Display answer
            st.markdown('<div class="answer-container">', unsafe_allow_html=True)
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
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        finally:
            st.session_state.processing = False
            st.rerun()

# Footer
st.markdown("""
    <div class="footer">
        Built with ❤️ using Streamlit, LangChain, and OpenAI
    </div>
""", unsafe_allow_html=True)
