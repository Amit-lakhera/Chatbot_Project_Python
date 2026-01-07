import streamlit as st
from transformers import pipeline

# Page config (mobile friendly)
st.set_page_config(
  page_title="AI Chatbot",
  page_icon="🤖",
  layout="centered"
)

st.title("🤖 AI Chatbot")
st.caption("Built with Streamlit + Hugging Face (No API key)")

# Load model only once
@st.cache_resource
def load_model():
  return pipeline(
    "text-generation",
    model="distilgpt2"
  )
  
generator = load_model()

# Initialize chat history
if "messages" not in st.session_state:
  st.session_state.messages = []

# Display chat history
for role, message in st.session_state.messages:
  if role == "You":
    st.markdown(f"🧑 **You:** {message}")
  else:
    st.markdown(f"🤖 **Bot:** {message}")

# User input
user_input = st.text_input(
  "Type your message:",
  placeholder="Ask something..."
)

# Generate response
if user_input:
  st.session_state.messages.append(("You", user_input))
  
  with st.spinner("Bot is thinking..."):
    response = generator(
      user_input,
      max_length=120,
      num_return_sequences=1,
      pad_token_id=50256
    )[0]["generated_text"]
    
    st.session_state.messages.append(("Bot", response))
    st.rerun()
