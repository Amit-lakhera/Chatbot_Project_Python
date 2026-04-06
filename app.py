import streamlit as st
from transformers import pipeline

st.title("🤖 AI Chatbot")

@st.cache_resource
def load_model():
    return pipeline("text2text-generation", model="t5-small")

chatbot = load_model()

# Greeting
def get_greeting_response(user_input):
    greetings = ["hi", "hello", "hey"]
    if user_input.lower() in greetings:
        return "Hello 👋! I'm your AI chatbot. How can I help you today?"
    return None

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    response = get_greeting_response(user_input)

    if response is None:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chatbot(user_input, max_length=100)[0]["generated_text"]
                st.write(response)
    else:
        with st.chat_message("assistant"):
            st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
