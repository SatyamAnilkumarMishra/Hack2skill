import streamlit as st
from crew_config import build_agent

# Build your agent
agent = build_agent()

st.set_page_config(page_title="AI Career Assistant", page_icon="🤖", layout="centered")
st.title("🤖 AI Career Assistant")
st.write("Ask me anything about your career path, AI skills, or opportunities!")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if query := st.chat_input("Type your question here..."):
    # Save user query
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Call your agent
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = agent.respond(context="career guidance", query=query, student_profile="AI enthusiast")
            st.markdown(response)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
