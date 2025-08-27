from crewai import Agent
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load Gemini key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def build_agent():
    class GeminiAgent(Agent):
        def respond(self, prompt):
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            return response.text

    return GeminiAgent(
        role="RAG Assistant",
        goal="Answer queries using retrieval augmented generation",
        backstory="An AI assistant powered by Google Gemini"
    )

