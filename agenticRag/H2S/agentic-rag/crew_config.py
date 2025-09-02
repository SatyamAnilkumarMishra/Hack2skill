from crewai import Agent

# Define your agent here
agent = Agent(
    role="career-guide",
    goal="Guide students on AI, ML, and software careers",
    backstory=(
        "You are an expert in AI, Machine Learning, Data Science, and career development. "
        "You help students by analyzing their interests and skills to suggest the best career paths."
    ),
)

# Function to return the agent (for app.py or main.py)
def build_agent():
    return agent
