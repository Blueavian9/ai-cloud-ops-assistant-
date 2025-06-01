import os
import streamlit as st
from dotenv import load_dotenv
from src.utils.document_loader import DocumentLoader
from src.utils.vector_store import VectorStore
from src.utils.qa_system import QASystem
from datetime import datetime

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
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "General"

# UI Configuration
st.set_page_config(
    page_title="Cloud Ops AI Assistant",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with professional styling
st.markdown("""
    <style>
    /* Global styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Theme variables */
    :root {
        --primary-color: #2563eb;
        --secondary-color: #3b82f6;
        --accent-color: #60a5fa;
        --bg-light: #ffffff;
        --bg-dark: #1a1a1a;
        --text-light: #1f2937;
        --text-dark: #f3f4f6;
        --border-light: #e5e7eb;
        --border-dark: #374151;
    }
    
    /* Main container */
    .main {
        padding: 2rem;
        max-width: 1400px;
        margin: 0 auto;
        min-height: 100vh;
    }
    
    /* Header styling */
    .header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .header-icon {
        font-size: 2rem;
        color: var(--primary-color);
    }
    
    /* Search container */
    .search-container {
        background: var(--bg-light);
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    .search-container.dark {
        background: var(--bg-dark);
        color: var(--text-dark);
    }
    
    /* Category pills */
    .category-pills {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 1rem;
        flex-wrap: wrap;
    }
    
    .category-pill {
        padding: 0.5rem 1rem;
        border-radius: 2rem;
        background: #f3f4f6;
        color: #4b5563;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .category-pill:hover {
        background: #e5e7eb;
    }
    
    .category-pill.active {
        background: var(--primary-color);
        color: white;
    }
    
    /* Question input */
    .question-input {
        width: 100%;
        padding: 1rem;
        border: 2px solid var(--border-light);
        border-radius: 0.5rem;
        font-size: 1rem;
        transition: all 0.2s ease;
    }
    
    .question-input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }
    
    /* Answer container */
    .answer-container {
        background: var(--bg-light);
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-top: 2rem;
    }
    
    .answer-container.dark {
        background: var(--bg-dark);
        color: var(--text-dark);
    }
    
    /* Source box */
    .source-box {
        background: #f9fafb;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
        border: 1px solid var(--border-light);
    }
    
    .source-box.dark {
        background: #2d3748;
        border-color: var(--border-dark);
    }
    
    /* Chat history */
    .chat-history {
        margin-top: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        max-width: 80%;
    }
    
    .chat-message.user {
        background: #e5e7eb;
        margin-left: auto;
    }
    
    .chat-message.assistant {
        background: #f3f4f6;
        margin-right: auto;
    }
    
    /* Action buttons */
    .action-button {
        background: var(--primary-color);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        border: none;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .action-button:hover {
        background: var(--secondary-color);
    }
    
    /* Loading animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f4f6;
        border-radius: 50%;
        border-top-color: var(--primary-color);
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
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
    st.markdown('<div class="header"><span class="header-icon">☁️</span><h1>Cloud Ops AI</h1></div>', unsafe_allow_html=True)
    
    st.markdown("### Quick Links")
    st.markdown("""
    - [AWS Documentation](https://docs.aws.amazon.com)
    - [AWS CLI Reference](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/index.html)
    - [AWS Well-Architected](https://aws.amazon.com/architecture/well-architected)
    """)
    
    st.markdown("### Categories")
    categories = ["General", "Security", "Compute", "Storage", "Networking", "Database", "DevOps"]
    for category in categories:
        if st.button(category, key=f"cat_{category}"):
            st.session_state.selected_category = category
            st.rerun()
    
    st.markdown("---")
    st.markdown("### Recent Questions")
    for msg in st.session_state.chat_history[-5:]:
        st.markdown(f"- {msg['content'][:50]}...")
    
    st.markdown("---")
    if st.button("🗑️ Clear History"):
        st.session_state.chat_history = []
        st.rerun()

# Main content
st.markdown('<div class="header"><span class="header-icon">☁️</span><h1>Cloud Ops AI Assistant</h1></div>', unsafe_allow_html=True)

# Category selection
st.markdown('<div class="category-pills">', unsafe_allow_html=True)
for category in ["General", "Security", "Compute", "Storage", "Networking", "Database", "DevOps"]:
    active = "active" if category == st.session_state.selected_category else ""
    st.markdown(f'<span class="category-pill {active}">{category}</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Search Interface
with st.container():
    st.markdown(f'<div class="search-container {st.session_state.theme}">', unsafe_allow_html=True)
    query = st.text_input(
        "Ask a cloud question",
        placeholder="e.g., 'How do I secure an S3 bucket?' or 'Explain EC2 instance types'",
        key="query_input"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        search_button = st.button("🔍 Search", use_container_width=True)
    with col2:
        if st.button("🌙 Toggle Theme"):
            st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

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

# Display chat history
if st.session_state.chat_history:
    st.markdown('<div class="chat-history">', unsafe_allow_html=True)
    for message in st.session_state.chat_history:
        st.markdown(f"""
            <div class="chat-message {message['role']}">
                <div class="content">{message['content']}</div>
                <div class="timestamp">{message['timestamp']}</div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Answer Display
if query and search_button:
    st.session_state.processing = True
    with st.spinner(""):
        st.markdown('<div class="loading"></div>', unsafe_allow_html=True)
        try:
            result = qa_system.answer_question(query)
            
            # Add to chat history
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
            st.markdown(f'<div class="answer-box">{result["answer"]}</div>', unsafe_allow_html=True)
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("📋 Copy Answer", key="copy_answer")
            with col2:
                st.button("💾 Save to Favorites", key="save_favorite")
            with col3:
                st.button("📤 Share", key="share")
            
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
st.markdown("""
    <div class="footer">
        <p>Built with ❤️ using Streamlit, LangChain, and OpenAI</p>
        <p>© 2024 Cloud Ops AI Assistant</p>
    </div>
""", unsafe_allow_html=True)
