import streamlit as st
import os
from crew_config import build_agent
from rag_pipeline import build_vector_store
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Agentic RAG Assistant", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = None
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "pdf_loaded" not in st.session_state:
    st.session_state.pdf_loaded = False

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Key status
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        st.success("✅ Google API Key loaded")
    else:
        st.error("❌ Google API Key not found")
        st.info("Please add your Google API Key to the .env file")
    
    st.divider()
    
    # PDF Upload
    st.subheader("📄 Document Upload")
    uploaded_file = st.file_uploader(
        "Upload a PDF document for RAG", 
        type=["pdf"],
        help="Upload a PDF to enable context-aware responses"
    )
    
    if uploaded_file:
        if st.button("Process PDF"):
            with st.spinner("Processing PDF..."):
                try:
                    # Save uploaded file
                    with open("temp_document.pdf", "wb") as f:
                        f.write(uploaded_file.getvalue())
                    
                    # Build vector store
                    st.session_state.vectorstore = build_vector_store("temp_document.pdf")
                    st.session_state.pdf_loaded = True
                    st.success("PDF processed successfully!")
                    
                    # Clean up temp file
                    if os.path.exists("temp_document.pdf"):
                        os.remove("temp_document.pdf")
                        
                except Exception as e:
                    st.error(f"Error processing PDF: {str(e)}")
                    logger.error(f"PDF processing error: {str(e)}")
    
    # Default document check
    if not st.session_state.pdf_loaded:
        if os.path.exists("Career_Advisor_Guide_2025.pdf"):
            if st.button("Load Default Document"):
                with st.spinner("Loading default document..."):
                    try:
                        st.session_state.vectorstore = build_vector_store("Career_Advisor_Guide_2025.pdf")
                        st.session_state.pdf_loaded = True
                        st.success("Default document loaded!")
                    except Exception as e:
                        st.error(f"Error loading default document: {str(e)}")
        else:
            st.info("No default document found. Upload a PDF to enable RAG.")
    
    st.divider()
    
    # Student Profile
    st.subheader("👤 Student Profile")
    student_profile = st.text_area(
        "Describe your background",
        value="AI enthusiast interested in machine learning and career development",
        height=100,
        help="This helps personalize responses to your background and interests"
    )
    
    st.divider()
    
    # Settings
    st.subheader("🔧 Settings")
    max_context_docs = st.slider(
        "Max context documents", 
        min_value=1, 
        max_value=10, 
        value=3,
        help="Number of relevant documents to retrieve for context"
    )
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Main interface
st.title("🤖 Agentic RAG Assistant")
st.markdown(
    "An intelligent assistant powered by Google Gemini with Retrieval-Augmented Generation capabilities."
)

# Status indicators
col1, col2, col3 = st.columns(3)
with col1:
    if api_key:
        st.success("🔑 API Connected")
    else:
        st.error("🔑 API Not Connected")

with col2:
    if st.session_state.agent:
        st.success("🤖 Agent Ready")
    else:
        st.warning("🤖 Agent Loading...")

with col3:
    if st.session_state.pdf_loaded:
        st.success("📄 RAG Enabled")
    else:
        st.info("📄 RAG Disabled")

st.divider()

# Initialize agent if not already done
if not st.session_state.agent and api_key:
    try:
        with st.spinner("Initializing AI agent..."):
            st.session_state.agent = build_agent()
        st.success("Agent initialized successfully!")
        st.rerun()
    except Exception as e:
        st.error(f"Failed to initialize agent: {str(e)}")
        logger.error(f"Agent initialization error: {str(e)}")

# Chat interface
if st.session_state.agent:
    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "timestamp" in msg:
                st.caption(f"*{msg['timestamp']}*")
    
    # User input
    if query := st.chat_input("Ask me anything about your career, AI, or upload a document for specific questions..."):
        # Add user message
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.messages.append({
            "role": "user", 
            "content": query,
            "timestamp": timestamp
        })
        
        with st.chat_message("user"):
            st.markdown(query)
            st.caption(f"*{timestamp}*")
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    context = ""
                    
                    # Retrieve context if RAG is enabled
                    if st.session_state.pdf_loaded and st.session_state.vectorstore:
                        try:
                            docs = st.session_state.vectorstore.similarity_search(
                                query, k=max_context_docs
                            )
                            context = "\n\n".join([d.page_content for d in docs])
                            
                            # Show retrieved context in expander
                            if context:
                                with st.expander("📚 Retrieved Context"):
                                    st.text(context[:500] + "..." if len(context) > 500 else context)
                        except Exception as e:
                            st.warning(f"Could not retrieve context: {str(e)}")
                            logger.warning(f"Context retrieval error: {str(e)}")
                    
                    # Generate response
                    if context:
                        response = st.session_state.agent.respond(
                            context=context, 
                            query=query, 
                            student_profile=student_profile
                        )
                    else:
                        response = st.session_state.agent.respond(
                            query=query, 
                            student_profile=student_profile
                        )
                    
                    st.markdown(response)
                    response_timestamp = datetime.now().strftime("%H:%M:%S")
                    st.caption(f"*{response_timestamp}*")
                    
                    # Add assistant message
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response,
                        "timestamp": response_timestamp
                    })
                    
                except Exception as e:
                    error_msg = f"I apologize, but I encountered an error: {str(e)}"
                    st.error(error_msg)
                    logger.error(f"Response generation error: {str(e)}")
                    
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": error_msg,
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })
else:
    st.info("🔄 Please ensure your Google API key is configured in the .env file to start chatting.")
    
    # Show sample .env content
    st.code("""
# Add this to your .env file:
GOOGLE_API_KEY=your_api_key_here
""", language="bash")