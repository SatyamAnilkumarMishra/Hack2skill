import os
from dotenv import load_dotenv
from rag_pipeline import build_vector_store
from crew_config import build_agent

# Load API key
load_dotenv()

def main():
    # Build agent & retriever
    agent = build_agent()
    vectorstore = build_vector_store("Career_Advisor_Guide_2025.pdf")

    print("Agentic RAG started with Gemini. Type 'exit' to quit.")

    while True:
        query = input("You: ")
        if query.lower() == "exit":
            break

        # Retrieve relevant docs
        docs = vectorstore.similarity_search(query, k=3)
        context = "\n".join([d.page_content for d in docs])

        # Ask the agent (adjust method if not respond)
        response = agent.respond(f"Context: {context}\n\nQuestion: {query}")
        print("Assistant:", response)

if __name__ == "__main__":
    main()
