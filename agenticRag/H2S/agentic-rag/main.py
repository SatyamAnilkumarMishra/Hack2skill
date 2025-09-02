# main.py
import os
from dotenv import load_dotenv
from rag_pipeline import build_vector_store
from crew_config import CareerAgent

# Load from .env if available
load_dotenv()

# Double-check env variable
if not os.getenv("COHERE_API_KEY"):
    print("⚠️ Warning: COHERE_API_KEY not found in .env, trying system environment variables...")
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("❌ COHERE_API_KEY not found! Please set it in .env or as a system environment variable.")
else:
    api_key = os.getenv("COHERE_API_KEY")

def get_student_profile():
    """Collect student profile details"""
    print("Please enter your profile details:")
    name = input("Name: ")
    education = input("Education (e.g., 12th, B.Tech, Diploma): ")
    skills = input("Skills (comma-separated): ").split(",")
    interests = input("Interests (comma-separated): ").split(",")
    return {
        "name": name.strip(),
        "education": education.strip(),
        "skills": [s.strip() for s in skills if s.strip()],
        "interests": [i.strip() for i in interests if i.strip()]
    }

def main():
    # Build agent & vector store
    agent = CareerAgent()
    vectorstore = build_vector_store("Career_Advisor_Guide_2025.pdf")

    student_profile = get_student_profile()

    print("\nPersonalized Career Advisor Started. Type 'exit' to quit.\n")

    while True:
        query = input("You: ")
        if query.lower() == "exit":
            break

        # Retrieve relevant docs from vector store
        docs = vectorstore.similarity_search(query, k=3)
        context = "\n".join([d.page_content for d in docs])

        # Ask the agent
        response = agent.respond(context, query, student_profile)
        print("\nAssistant:\n", response)
        print("-" * 80)

if __name__ == "__main__":
    main()
