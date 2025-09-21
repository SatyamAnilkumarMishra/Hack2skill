import os
import sys
from dotenv import load_dotenv
from rag_pipeline import build_vector_store
from crew_config import build_agent
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def main():
    """Main CLI interface for the Agentic RAG system"""
    try:
        # Check for API key
        if not os.getenv("GOOGLE_API_KEY"):
            print("❌ Error: GOOGLE_API_KEY not found in environment variables.")
            print("Please add your Google API key to the .env file:")
            print("GOOGLE_API_KEY=your_api_key_here")
            sys.exit(1)
        
        print("🤖 Initializing Agentic RAG Assistant...")
        
        # Build agent
        try:
            agent = build_agent()
            print("✅ Agent initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize agent: {str(e)}")
            sys.exit(1)
        
        # Check for default PDF and build vector store
        vectorstore = None
        pdf_path = "Career_Advisor_Guide_2025.pdf"
        
        if os.path.exists(pdf_path):
            try:
                print(f"📄 Loading document: {pdf_path}")
                vectorstore = build_vector_store(pdf_path)
                print("✅ Vector store built successfully")
            except Exception as e:
                print(f"⚠️  Warning: Could not build vector store: {str(e)}")
                print("🔄 Continuing in basic mode without RAG...")
        else:
            print(f"⚠️  Warning: Default document '{pdf_path}' not found")
            print("🔄 Running in basic mode without RAG...")
        
        print("\n" + "="*50)
        print("🚀 Agentic RAG Assistant is ready!")
        if vectorstore:
            print("📚 RAG mode: Enabled")
        else:
            print("💬 Basic mode: No document context")
        print("Type 'exit', 'quit', or 'q' to quit.")
        print("="*50 + "\n")
        
        # Main conversation loop
        while True:
            try:
                query = input("You: ").strip()
                
                if not query:
                    continue
                    
                if query.lower() in ['exit', 'quit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                print("🤔 Thinking...")
                
                # Retrieve relevant docs if vectorstore is available
                context = ""
                if vectorstore:
                    try:
                        docs = vectorstore.similarity_search(query, k=3)
                        context = "\n\n".join([d.page_content for d in docs])
                        if context:
                            print(f"📖 Retrieved {len(docs)} relevant document(s)")
                    except Exception as e:
                        logger.warning(f"Context retrieval failed: {str(e)}")
                
                # Generate response
                try:
                    if context:
                        response = agent.respond(context=context, query=query)
                    else:
                        response = agent.respond(query=query)
                    
                    print(f"\nAssistant: {response}\n")
                    
                except Exception as e:
                    print(f"❌ Error generating response: {str(e)}")
                    logger.error(f"Response generation failed: {str(e)}")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {str(e)}")
                logger.error(f"Unexpected error in main loop: {str(e)}")
                
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        logger.error(f"Fatal error in main: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
