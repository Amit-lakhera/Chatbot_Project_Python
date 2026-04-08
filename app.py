import streamlit as st
from datetime import datetime
import pytz

st.title("🤖 Chatbot")

# Indian Time Zone
ist = pytz.timezone("Asia/Kolkata")

# -------------------------
# RESPONSE FUNCTION
# -------------------------

def chatbot_response(user_input):
    text = user_input.lower()

    # Greeting
    if text in ["hi", "hello", "hey", "hii"]:
        return "Hello 👋! I'm your chatbot. How can I help you today?"

    # Thanks
    if "thank" in text:
        return "You're welcome 😊! Happy to help. Have a great day!"

    # Get IST time
    now = datetime.now(ist)
    current_time = now.strftime("%I:%M %p")
    current_date = now.strftime("%d-%m-%Y")

    # Only time
    if "time" in text and "date" not in text:
        return f"⏰ Current Time (IST): {current_time}"

    # Only date
    if "date" in text and "time" not in text:
        return f"📅 Today's Date: {current_date}"

    # Both date & time
    if "date" in text and "time" in text:
        return f"📅 Date: {current_date}\n⏰ Time (IST): {current_time}"

    # Default
    return "I can respond to greetings, thanks, and date/time 😊"

# -------------------------
# CHAT SYSTEM
# -------------------------

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

    response = chatbot_response(user_input)

    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
