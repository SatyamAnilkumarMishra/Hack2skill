# 🤖 Agentic RAG Assistant

An intelligent Retrieval-Augmented Generation (RAG) system powered by Google Gemini with both web and command-line interfaces.

## ✨ Features

- **🧠 AI-Powered Responses**: Uses Google Gemini 1.5 Flash for intelligent conversations
- **📚 Document Understanding**: Upload PDFs for context-aware responses using RAG
- **🌐 Web Interface**: Beautiful Streamlit web app with modern UI
- **💻 CLI Interface**: Command-line interface for terminal users
- **📄 PDF Processing**: Automatic text extraction and vector embedding
- **🔍 Semantic Search**: Find relevant information from your documents
- **⚙️ Configurable**: Customize chunk sizes, context length, and more
- **🔒 Secure**: Environment-based API key management

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install required packages
python run.py install

# Or manually:
pip install -r requirements.txt
```

### 2. Setup Environment

```bash
# Create .env file template
python run.py setup

# Then edit .env and add your Google API key:
# GOOGLE_API_KEY=your_google_api_key_here
```

### 3. Run the Application

```bash
# Start web interface (recommended)
python run.py web

# Or start CLI interface
python run.py cli

# Check project status
python run.py status
```

## 📋 Requirements

- Python 3.8+
- Google API key (Gemini API access)
- 2GB+ RAM (for embeddings model)
- Internet connection (for API calls)

## 🛠️ Installation

### Method 1: Using the Runner Script (Recommended)

```bash
# Clone/download the project
cd agentic-rag

# Install everything
python run.py install

# Setup environment
python run.py setup

# Edit .env file with your API key
# Then start the web interface
python run.py web
```

### Method 2: Manual Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# Start Streamlit
streamlit run app.py

# Or CLI
python main.py
```

## 🖥️ Interfaces

### Web Interface (Streamlit)

The web interface provides:
- **📊 Status Dashboard**: See API, agent, and RAG status
- **📤 File Upload**: Upload PDFs for processing
- **💬 Chat Interface**: Interactive conversation with timestamps
- **👤 Student Profile**: Personalize responses to your background
- **⚙️ Settings**: Adjust context documents and other parameters
- **📚 Context Display**: View retrieved document snippets

```bash
python run.py web
# Opens in browser at http://localhost:8501
```

### Command Line Interface

The CLI provides:
- **🔍 Context Retrieval**: Automatic document search
- **💡 Smart Responses**: Context-aware AI responses
- **📈 Progress Indicators**: Visual feedback during processing
- **⚡ Fast Setup**: Quick initialization and document loading

```bash
python run.py cli
# Interactive terminal interface
```

## 📁 Project Structure

```
agentic-rag/
├── app.py              # Streamlit web interface
├── main.py             # CLI interface
├── crew_config.py      # AI agent configuration
├── rag_pipeline.py     # Document processing pipeline
├── run.py              # Project runner script
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
├── README.md          # This file
└── chroma_db/         # Vector database (auto-created)
```

## ⚙️ Configuration

### Environment Variables (.env)

```bash
# Required
GOOGLE_API_KEY=your_google_api_key_here

# Optional
LOG_LEVEL=INFO
```

### RAG Settings

You can customize the RAG pipeline in `rag_pipeline.py`:

- `chunk_size`: Size of text chunks (default: 500)
- `chunk_overlap`: Overlap between chunks (default: 50)
- `max_context_docs`: Number of documents to retrieve (default: 3)

### Agent Settings

Modify the AI agent in `crew_config.py`:

- Model: `gemini-1.5-flash` (default)
- Temperature and other generation parameters
- System prompts and behavior

## 📚 Usage Examples

### Basic Conversation

```bash
You: What are the key skills needed for AI careers?
Assistant: Based on current industry trends, key skills for AI careers include...
```

### Document-Based Questions

1. Upload a PDF through the web interface or place it in the project directory
2. Ask questions related to the document content
3. The system will retrieve relevant context and provide informed answers

```bash
You: What does the document say about machine learning techniques?
📖 Retrieved 3 relevant document(s)
Assistant: According to the document, machine learning techniques include...
```

### Student Profile Customization

Set your background in the web interface:
```
AI enthusiast with a background in computer science, 
interested in machine learning and career development
```

This personalizes responses to your specific situation and interests.

## 🐛 Troubleshooting

### Common Issues

**"Google API Key not found"**
```bash
# Check .env file exists and contains your API key
python run.py status
```

**"PDF processing failed"**
```bash
# Ensure PDF is text-based (not scanned images)
# Check file permissions and disk space
```

**"Module not found"**
```bash
# Reinstall dependencies
python run.py install
```

**"Streamlit port already in use"**
```bash
# Use different port
streamlit run app.py --server.port 8502
```

### Debug Mode

For detailed logging, set environment variable:
```bash
LOG_LEVEL=DEBUG python main.py
```

## 🔧 Development

### Adding New Features

1. **New document types**: Modify `rag_pipeline.py` loaders
2. **Custom embeddings**: Update embedding model in `rag_pipeline.py`
3. **UI improvements**: Edit `app.py` Streamlit components
4. **Agent behavior**: Modify prompts in `crew_config.py`

### Testing

```bash
# Run basic functionality test
python run.py status

# Test web interface
python run.py web
# Navigate to localhost:8501 and test features

# Test CLI interface
python run.py cli
# Try various queries and document uploads
```

## 📄 API Keys

### Getting Google API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Create a new project or select existing one
4. Generate an API key
5. Add it to your `.env` file

### Rate Limits

- Gemini API has request limits
- For production use, consider implementing rate limiting
- Monitor your API usage in Google Cloud Console

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is provided as-is for educational and development purposes.

## 🆘 Support

For issues and questions:

1. Check the troubleshooting section
2. Review the project status: `python run.py status`
3. Check logs for error messages
4. Ensure all requirements are installed

## 🔮 Future Enhancements

- [ ] Support for more document formats (Word, TXT, etc.)
- [ ] Multiple AI model support (OpenAI, Anthropic, etc.)
- [ ] Advanced RAG techniques (HyDE, ReAct, etc.)
- [ ] User authentication and session management
- [ ] Document management interface
- [ ] API endpoint for integration
- [ ] Docker containerization
- [ ] Cloud deployment guides

---

**Happy coding! 🚀**

*Built with ❤️ using Streamlit, LangChain, and Google Gemini*