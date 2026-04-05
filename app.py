import streamlit as st
from transformers import pipeline
import json
import requests
from datetime import datetime

st.set_page_config(page_title="Premium AI Chatbot", layout="wide")

# ---------------- LOGIN SYSTEM ---------------- #
def load_users():
    with open("users.json") as f:
        return json.load(f)

def login():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = load_users()
        if username in users and users[username] == password:
            st.session_state.user = username
            st.success("Login Successful")
        else:
            st.error("Invalid Credentials")

if "user" not in st.session_state:
    login()
    st.stop()

# ---------------- LOAD MODEL ---------------- #
@st.cache_resource
def load_model():
    return pipeline(
        "text-generation",
        model="distilgpt2"
    )

chatbot = load_model()

# ---------------- MEMORY ---------------- #
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_logs" not in st.session_state:
    st.session_state.chat_logs = []

# ---------------- INTERNET SEARCH ---------------- #
def search_web(query):
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        data = requests.get(url).json()
        return data.get("Abstract", "")
    except:
        return ""

# ---------------- PROMPT BUILDER ---------------- #
def build_prompt(messages, user_input):
    context = ""
    for msg in messages[-5:]:
        role = "User" if msg["role"] == "user" else "Assistant"
        context += f"{role}: {msg['content']}\n"
    context += f"User: {user_input}\nAssistant:"
    return context

# ---------------- UI ---------------- #
st.title(f"🤖 Premium Chatbot | Welcome {st.session_state.user}")

menu = st.sidebar.selectbox("Menu", ["Chat", "Dashboard"])

# ---------------- CHAT ---------------- #
if menu == "Chat":
    use_internet = st.sidebar.checkbox("🌐 Enable Internet")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Ask anything...")

    if user_input:
        with st.chat_message("user"):
            st.write(user_input)

        # Internet enhancement
        if use_internet:
            web_data = search_web(user_input)
            if web_data:
                user_input += f" (Context: {web_data})"

        prompt = build_prompt(st.session_state.messages, user_input)

        with st.spinner("Thinking..."):
            response = chatbot(
                prompt,
                max_length=150,
                do_sample=True,
                temperature=0.7
            )

        bot_reply = response[0]["generated_text"]

        with st.chat_message("assistant"):
            st.write(bot_reply)

        # Save chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

        # Logs for dashboard
        st.session_state.chat_logs.append({
            "user": st.session_state.user,
            "query": user_input,
            "response": bot_reply,
            "time": str(datetime.now())
        })

# ---------------- DASHBOARD ---------------- #
if menu == "Dashboard":
    st.title("📊 Admin Dashboard")

    logs = st.session_state.chat_logs
    st.write(f"Total Chats: {len(logs)}")

    if logs:
        for log in logs[-10:]:
            st.write(log)

# ---------------- SIDEBAR ---------------- #
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.sidebar.success("Chat cleared!")
