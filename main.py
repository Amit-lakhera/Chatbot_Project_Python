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

# ---------------- Chat Memory ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for role, msg in st.session_state.messages:
    st.markdown(f"**{role}:** {msg}")

# ---------------- Helper: Fetch News ----------------
def get_latest_news():
    feed = feedparser.parse("https://feeds.bbci.co.uk/news/rss.xml")
    news_items = []
    for entry in feed.entries[:5]:
        news_items.append(f"- {entry.title}")
    return "\n".join(news_items)

# ---------------- User Input ----------------
user_input = st.text_input("You:", placeholder="Ask a question or type 'latest news'")

if user_input:
    st.session_state.messages.append(("You", user_input))

    with st.spinner("Thinking..."):

        # -------- News Query --------
        if "news" in user_input.lower():
            news = get_latest_news()
            prompt = f"Summarize these news headlines briefly:\n{news}"
            response = llm(prompt, max_new_tokens=120)[0]["generated_text"]

        # -------- Normal Question --------
        else:
            prompt = f"Answer clearly and briefly:\n{user_input}"
            response = llm(prompt, max_new_tokens=80)[0]["generated_text"]

    st.session_state.messages.append(("Bot", response))
    st.rerun()
