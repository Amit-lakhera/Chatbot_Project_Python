import streamlit as st
import openai

# ------------------ Page Config ------------------
st.set_page_config(page_title="Chatbot using OpenAI", page_icon="🤖")

# ------------------ OpenAI API Key ------------------
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ------------------ Title ------------------
st.title("🤖 Chatbot using Streamlit and OpenAI")

# ------------------ Session State ------------------
if "messages" not in st.session_state:
  st.session_state.messages = []

# ------------------ Chat Display ------------------
for msg in st.session_state.messages:
  with st.chat_message(msg["role"]):
    st.markdown(msg["content"])

# ------------------ User Input ------------------
user_input = st.chat_input("Type your message here...")

# ------------------ Generate Response ------------------
if user_input:
    # Show user message
    st.session_state.messages.append(
      {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
      st.markdown(user_input)

    # Call OpenAI API
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
        messages=st.session_state.messages,
        max_tokens=300
    )

    bot_reply = response.choices[0].message.content

    # Show assistant message
    st.session_state.messages.append(
      {"role": "assistant", "content": bot_reply}
    )

    with st.chat_message("assistant"):
      st.markdown(bot_reply)
