import streamlit as st
from datetime import datetime
import pytz
import requests
import wikipedia
from duckduckgo_search import DDGS

st.set_page_config(page_title="Ultimate AI Assistant", page_icon="🤖")
st.title("🤖 Ultimate AI Assistant")

ist = pytz.timezone("Asia/Kolkata")

# -------------------------
# 🌍 SMART LEADER FETCH (PM / PRESIDENT / CM)
# -------------------------
def get_leader_info(user_input):
    text = user_input.lower()

    try:
        if any(x in text for x in ["prime minister", "pm of"]):
            country = text.split("of")[-1].strip()
            result = wikipedia.summary(f"Prime Minister of {country}", sentences=1)
            return f"🌍 {result}"

        if "president" in text:
            country = text.split("of")[-1].strip()
            result = wikipedia.summary(f"President of {country}", sentences=1)
            return f"🌍 {result}"

        if "chief minister" in text or "cm of" in text:
            state = text.split("of")[-1].strip()
            result = wikipedia.summary(f"Chief Minister of {state}", sentences=1)
            return f"🏛️ {result}"

    except:
        return None

    return None

# -------------------------
# 🎉 FESTIVAL INFO
# -------------------------
def get_festival_info(user_input):
    text = user_input.lower()

    if "diwali" in text:
        if "why" in text:
            return "🪔 Diwali marks Lord Rama’s return to Ayodhya and symbolizes victory of light over darkness."
        if "when" in text:
            return "🎉 Diwali 2026 is on 8 November 2026"

    if "holi" in text:
        if "why" in text:
            return "🌈 Holi celebrates victory of Prahlad and arrival of spring."
        if "when" in text:
            return "🎉 Holi 2026 is on 3 March 2026"

    return None

# -------------------------
# 🌦 WEATHER
# -------------------------
def extract_city(text):
    remove = ["weather", "in", "of", "what", "is", "the"]
    return " ".join([w for w in text.lower().split() if w not in remove])


def get_weather(city):
    try:
        geo = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&country=India").json()
        lat = geo["results"][0]["latitude"]
        lon = geo["results"][0]["longitude"]

        data = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true").json()

        temp = data["current_weather"]["temperature"]
        wind = data["current_weather"]["windspeed"]

        return f"🌦️ {city.title()}: {temp}°C, Wind {wind} km/h"
    except:
        return "❌ Weather not found"

# -------------------------
# 📚 WIKIPEDIA
# -------------------------
def get_wikipedia(query):
    try:
        return wikipedia.summary(query, sentences=3)
    except:
        return None

# -------------------------
# 🌐 SEARCH
# -------------------------
def search_web(query):
    try:
        with DDGS() as ddgs:
            return list(ddgs.text(query, max_results=3))
    except:
        return None

# -------------------------
# 🧠 MAIN RESPONSE ENGINE
# -------------------------
def chatbot_response(user_input):
    text = user_input.lower()

    # Greetings
    if text in ["hi", "hello", "hey"]:
        return "Hello 👋! I'm your Ultimate AI Assistant."

    # Thanks
    if "thank" in text:
        return "You're welcome 😊"

    # Time & Date
    now = datetime.now(ist)
    if "time" in text:
        return now.strftime("⏰ %I:%M %p")

    if "date" in text:
        return now.strftime("📅 %d-%m-%Y")

    # Leaders (TOP PRIORITY)
    leader = get_leader_info(user_input)
    if leader:
        return leader

    # Weather
    if "weather" in text:
        city = extract_city(user_input)
        return get_weather(city)

    # Festival
    fest = get_festival_info(user_input)
    if fest:
        return fest

    # Wikipedia
    wiki = get_wikipedia(user_input)
    if wiki:
        return wiki

    # Web search
    web = search_web(user_input)
    if web:
        return web

    return "🤖 Sorry, I couldn't understand."

# -------------------------
# 💬 CHAT UI
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask anything...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            response = chatbot_response(user_input)

        if isinstance(response, list):
            st.markdown("### 🌐 Results")
            for r in response:
                st.markdown(f"**{r['title']}**\n{r.get('body','')}\n[Read more]({r['href']})")
                st.markdown("---")
        else:
            st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": str(response)})
