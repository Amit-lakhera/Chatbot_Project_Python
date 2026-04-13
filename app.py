import streamlit as st
import sqlite3

# Function to connect DB
def get_connection():
    return sqlite3.connect("agriculture.db")

# Function to fetch response
def get_response(user_input):
    conn = get_connection()
    cursor = conn.cursor()

    user_input = user_input.lower()

    # Fetch all data
    cursor.execute("SELECT keyword, response FROM agriculture")
    rows = cursor.fetchall()

    conn.close()

    for keyword, response in rows:
        if keyword in user_input:
            return response

    return "Sorry, I don't have information about that."

# Streamlit UI
st.set_page_config(page_title="Agri Chatbot", page_icon="🌾")

st.title("🌾 Agriculture Chatbot (SQLite)")
st.write("Ask anything about Indian agriculture!")

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("You:", "")

if st.button("Send"):
    if user_input:
        response = get_response(user_input)

        st.session_state.messages.append(("You", user_input))
        st.session_state.messages.append(("Bot", response))

# Display chat
for sender, msg in st.session_state.messages:
    if sender == "You":
        st.write(f"🧑 {msg}")
    else:
        st.write(f"🤖 {msg}")
