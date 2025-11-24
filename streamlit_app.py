import streamlit as st
from workflow.rag_workflow import rag_agent_orchestrator
st.write("Streamlit UI Loaded!")   # DEBUG LINE

st.set_page_config(page_title="RAG Assistant Demo", layout="centered")

st.title("🤖 RAG Agent Demo")
st.write("Ask a question and the agent will fetch weather or answer from PDF.")

# Maintain chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    role = "🧑‍💻 You" if msg["role"] == "user" else "🤖 Assistant"
    st.chat_message(msg["role"]).write(f"**{role}:** {msg['content']}")

# Input
user_input = st.chat_input("Type your message")

if user_input:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Call your RAG pipeline
    with st.spinner("Thinking..."):
        response = rag_agent_orchestrator(user_input)

    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
