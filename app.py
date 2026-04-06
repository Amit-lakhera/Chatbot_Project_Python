import streamlit as st
import json
import requests
from datetime import datetime

st.set_page_config(page_title="Amit AI Chatbot", layout="wide")

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

# ---------------- LOAD FLAN-T5 ---------------- #
@st.cache_resource
def load_model():
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

    model_name = "google/flan-t5-small"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    return tokenizer, model

tokenizer, model = load_model()

# ---------------- RESPONSE FUNCTION ---------------- #
def generate_response(prompt):
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)

    outputs = model.generate(
        **inputs,
        max_new_tokens=80,
        temperature=0.6,
        do_sample=True
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Clean unwanted phrases
    response = response.replace("Google Assistant", "")
    response = response.replace("I am an AI developed by Google", "")

    return response.strip()

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
        if msg["role"] == "user":
            context += f"User: {msg['content']}\n"
        else:
            context += f"Assistant: {msg['content']}\n"

    prompt = f"""
You are a chatbot named "Amit AI".
You are NOT Google Assistant or Alexa.
You are a helpful, friendly chatbot.

Rules:
- Do NOT mention Google Assistant or any company
- Keep answers short and clear
- Be conversational

{context}
User: {user_input}
Assistant:
"""
    return prompt

# ---------------- UI ---------------- #
st.title(f"🤖 Amit AI Chatbot | Welcome {st.session_state.user}")

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

        # Internet context
        if use_internet:
            web_data = search_web(user_input)
            if web_data:
                user_input += f" (Context: {web_data})"

        prompt = build_prompt(st.session_state.messages, user_input)

        with st.spinner("Thinking..."):
            bot_reply = generate_response(prompt)

        with st.chat_message("assistant"):
            st.write(bot_reply)

        # Save messages
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

        # Save logs
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
