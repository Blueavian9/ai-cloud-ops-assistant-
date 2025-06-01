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

# Custom CSS with cool features and dark mode support
st.markdown("""
    <style>
    /* Global styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Theme variables */
    :root {
        --bg-gradient-light: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
        --bg-gradient-dark: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        --text-color-light: #333333;
        --text-color-dark: #ffffff;
        --container-bg-light: rgba(255, 255, 255, 0.9);
        --container-bg-dark: rgba(45, 45, 45, 0.9);
        --border-color-light: rgba(255, 255, 255, 0.2);
        --border-color-dark: rgba(255, 255, 255, 0.1);
    }
    
    /* Main container with theme support */
    .main {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
        min-height: 100vh;
        transition: all 0.3s ease;
    }
    
    .main.light {
        background: var(--bg-gradient-light);
        color: var(--text-color-light);
    }
    
    .main.dark {
        background: var(--bg-gradient-dark);
        color: var(--text-color-dark);
    }
    
    /* Animated header with theme support */
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
    
    /* Enhanced search container with theme support */
    .search-container {
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        transition: all 0.3s ease;
    }
    
    .search-container.light {
        background: var(--container-bg-light);
        border: 1px solid var(--border-color-light);
    }
    
    .search-container.dark {
        background: var(--container-bg-dark);
        border: 1px solid var(--border-color-dark);
    }
    
    .search-container:hover {
        transform: translateY(-2px);
    }
    
    /* Enhanced input styling with theme support */
    .stTextInput>div>div>input {
        font-size: 1.2rem;
        padding: 1rem;
        border-radius: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input.light {
        background: var(--container-bg-light);
        border: 2px solid #e0e0e0;
        color: var(--text-color-light);
    }
    
    .stTextInput>div>div>input.dark {
        background: var(--container-bg-dark);
        border: 2px solid #404040;
        color: var(--text-color-dark);
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #4CAF50;
        box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.2);
        transform: scale(1.01);
    }
    
    /* Enhanced answer container with theme support */
    .answer-container {
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin-top: 2rem;
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease-out;
    }
    
    .answer-container.light {
        background: var(--container-bg-light);
        border: 1px solid var(--border-color-light);
    }
    
    .answer-container.dark {
        background: var(--container-bg-dark);
        border: 1px solid var(--border-color-dark);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Enhanced answer box with theme support */
    .answer-box {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
        transition: all 0.3s ease;
    }
    
    .answer-box.light {
        background: #ffffff;
        border: 2px solid #e0e0e0;
    }
    
    .answer-box.dark {
        background: #2d2d2d;
        border: 2px solid #404040;
    }
    
    /* Enhanced source box with theme support */
    .source-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .source-box.light {
        background: #ffffff;
        border: 1px solid #e0e0e0;
    }
    
    .source-box.dark {
        background: #2d2d2d;
        border: 1px solid #404040;
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
    
    /* Enhanced chat message styling with theme support */
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
        animation: slideIn 0.3s ease-out;
        position: relative;
    }
    
    .chat-message.light {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    }
    
    .chat-message.dark {
        background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .chat-message.user {
        margin-left: 20%;
        border-left: 4px solid #2196F3;
    }
    
    .chat-message.assistant {
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
    
    /* Theme toggle button */
    .theme-toggle {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 1000;
        background: linear-gradient(90deg, #4CAF50, #2196F3);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 2rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .theme-toggle:hover {
        transform: scale(1.05);
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
    
    /* Footer styling with theme support */
    .footer {
        text-align: center;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    .footer.light {
        color: #666;
    }
    
    .footer.dark {
        color: #999;
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

# Theme toggle function
def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

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
    - Dark mode support
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

# Theme toggle button
if st.button("🌙 Toggle Theme", key="theme_toggle"):
    toggle_theme()
    st.rerun()

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
    st.markdown(f'<div class="search-container {st.session_state.theme}">', unsafe_allow_html=True)
    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_input(
            "Ask a cloud question",
            placeholder="e.g., 'How do I use AWS CLI?' or 'Explain EC2 instance types'",
            label_visibility="collapsed",
            key="query_input"
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
                <div class="chat-message {message['role']} {st.session_state.theme}">
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
            st.markdown(f'<div class="answer-container {st.session_state.theme}">', unsafe_allow_html=True)
            st.markdown("### 💡 Answer")
            answer_container = st.container()
            with answer_container:
                st.markdown(f'<div class="answer-box {st.session_state.theme}">{result["answer"]}</div>', 
                           unsafe_allow_html=True)
                st.button("📋 Copy Answer", key="copy_answer")
            
            # Display sources
            if result["sources"]:
                st.markdown("### 📚 Sources")
                for i, source in enumerate(result["sources"], 1):
                    with st.expander(f"Source {i}"):
                        st.markdown(f'<div class="source-box {st.session_state.theme}">{source["content"]}</div>',
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
st.markdown(f"""
    <div class="footer {st.session_state.theme}">
        Built with ❤️ using Streamlit, LangChain, and OpenAI
    </div>
""", unsafe_allow_html=True)
