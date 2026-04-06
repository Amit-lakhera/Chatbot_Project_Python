import streamlit as st
from transformers import pipeline
import requests

st.title("🤖 Smart AI Chatbot")

# Load model
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="distilgpt2")

chatbot = load_model()

# -------------------------
# RULE-BASED RESPONSES
# -------------------------

def get_custom_response(user_input):
    text = user_input.lower()

    # Greeting
    if text in ["hi", "hello", "hey"]:
        return "Hello 👋! I'm your smart AI chatbot. How can I assist you today?"

    # Thanks response
    if "thank" in text:
        return "You're welcome 😊! Happy to help. If you have more questions, just ask!"

    # Weather (using free API)
    if "weather" in text:
        return get_weather()

    # Sports (basic)
    if "score" in text or "match" in text or "sports" in text:
        return "⚽ Sports update feature coming soon! (You can integrate live API here)"

    return None

# -------------------------
# WEATHER FUNCTION
# -------------------------

def get_weather():
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=21.25&longitude=81.63&current_weather=true"
        data = requests.get(url).json()

        temp = data["current_weather"]["temperature"]
        wind = data["current_weather"]["windspeed"]

        return f"🌦️ Current weather:\nTemperature: {temp}°C\nWind Speed: {wind} km/h"
    except:
        return "Sorry, I couldn't fetch weather right now."

# -------------------------
# CHAT HISTORY
# -------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# -------------------------
# USER INPUT
# -------------------------

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    # Custom logic first
    response = get_custom_response(user_input)

    # If no custom response → use AI model
    if response is None:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = chatbot(user_input, max_length=100, num_return_sequences=1)
                response = result[0]["generated_text"]
                st.write(response)
    else:
        with st.chat_message("assistant"):
            st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
