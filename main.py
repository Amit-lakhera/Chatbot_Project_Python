import streamlit as st
import feedparser
from transformers import pipeline

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Smart AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Smart AI Chatbot")
st.caption("Accurate • Fast • Live News (No Paid API)")

# ---------------- Load Model ----------------
@st.cache_resource
def load_model():
    return pipeline(
        "text2text-generation",
        model="google/flan-t5-base"
    )

llm = load_model()

# ---------------- Chat History ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages
for role, msg in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(msg)

# ---------------- Helper: Live News ----------------
def get_latest_news():
    feed = feedparser.parse("https://feeds.bbci.co.uk/news/rss.xml")
    headlines = [entry.title for entry in feed.entries[:5]]
    return "\n".join(headlines)

# ---------------- Chat Input (IMPORTANT FIX) ----------------
user_input = st.chat_input("Type your message...")

if user_input:

    # Show user message
    st.session_state.messages.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # Bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            # Greeting handling
            if user_input.lower().strip() in ["hi", "hello", "hey", "hii"]:
                response = "Hello! 😊 How can I help you today?"

            # News handling
            elif "news" in user_input.lower():
                news = get_latest_news()
                prompt = f"Summarize these headlines briefly:\n{news}"
                response = llm(prompt, max_new_tokens=120)[0]["generated_text"]

            # Normal questions
            else:
                prompt = f"Answer briefly and clearly:\n{user_input}"
                response = llm(prompt, max_new_tokens=80)[0]["generated_text"]

            st.markdown(response)

    st.session_state.messages.append(("assistant", response))
