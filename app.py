import streamlit as st

st.title("🤖 Chatbot")

# -------------------------
# RESPONSE FUNCTION
# -------------------------

def chatbot_response(user_input):
    text = user_input.lower()

    # Greeting responses
    if text in ["hi", "hello", "hey", "hii"]:
        return "Hello 👋! I'm your chatbot. How can I help you today?"

    # Thanks response
    if "thank" in text:
        return "You're welcome 😊! Happy to help. Have a great day!"

    # Default response
    return "I can respond to greetings and thanks for now 😊"

# -------------------------
# CHAT SYSTEM
# -------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    response = chatbot_response(user_input)

    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
