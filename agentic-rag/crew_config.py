import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class GeminiRAGAgent:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        
        self.role = "RAG Assistant"
        self.goal = "Answer queries using retrieval augmented generation"
        self.backstory = "An AI assistant powered by Google Gemini that provides accurate responses based on retrieved context"
        
        logger.info("GeminiRAGAgent initialized successfully")
    
    def respond(self, context="", query="", student_profile=""):
        """Generate response based on context and query"""
        try:
            if context and query:
                prompt = f"""Context: {context}
                
Query: {query}
                
Based on the provided context, please provide a helpful and accurate response to the query. If the context doesn't contain relevant information, acknowledge this and provide general guidance."""
            elif query:
                prompt = f"""Query: {query}
                
Student Profile: {student_profile}
                
Please provide helpful career guidance and advice based on the query."""
            else:
                prompt = context or "Hello! How can I help you today?"
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return f"I apologize, but I encountered an error while processing your request: {str(e)}"

def build_agent():
    """Build and return a GeminiRAGAgent instance"""
    try:
        return GeminiRAGAgent()
    except Exception as e:
        logger.error(f"Failed to build agent: {str(e)}")
        raise

