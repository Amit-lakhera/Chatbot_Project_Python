import streamlit as st
from datetime import datetime
import pytz
import requests
import wikipedia
from duckduckgo_search import DDGS

st.set_page_config(page_title="Smart AI Chatbot", page_icon="🤖")
st.title("🤖 Smart AI Chatbot (Advanced)")

# IST Timezone
ist = pytz.timezone("Asia/Kolkata")

# -------------------------
# WEATHER FUNCTIONS
# -------------------------
def extract_city(user_input):
    text = user_input.lower()
    remove_words = ["weather", "in", "of", "what", "is", "the", "tell", "me"]
    return " ".join([w for w in text.split() if w not in remove_words])


def get_coordinates(city):
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&country=India"
        data = requests.get(url).json()
        return data["results"][0]["latitude"], data["results"][0]["longitude"]
    except:
        return None, None


def get_weather(city):
    lat, lon = get_coordinates(city)
    if lat is None:
        return "❌ Location not found"

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    data = requests.get(url).json()

    temp = data["current_weather"]["temperature"]
    wind = data["current_weather"]["windspeed"]

    return f"🌦️ Weather in {city.title()}: {temp}°C, Wind {wind} km/h"

# -------------------------
# SMART FESTIVAL INFO
# -------------------------
def get_festival_info(user_input):
    text = user_input.lower()

    if "diwali" in text:
        if "why" in text:
            return "🪔 Diwali is celebrated to mark Lord Rama's return to Ayodhya after defeating Ravana. It represents victory of light over darkness."
        if "when" in text:
            return "🎉 Diwali 2026 is on 8 November 2026"

    if "holi" in text:
        if "why" in text:
            return "🌈 Holi celebrates the victory of Prahlad over Holika and the arrival of spring."
        if "when" in text:
            return "🎉 Holi 2026 is on 3 March 2026"

    return None

# -------------------------
# SMART WIKIPEDIA
# -------------------------
def get_wikipedia(query):
    try:
        results = wikipedia.search(query)
        if not results:
            return None

        page = wikipedia.page(results[0])
        return wikipedia.summary(results[0], sentences=4)

    except wikipedia.exceptions.DisambiguationError as e:
        return wikipedia.summary(e.options[0], sentences=2)
    except:
        return None

# -------------------------
# WEB SEARCH
# -------------------------
def search_web(query):
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=5):
                results.append(r)
        return results
    except:
        return None

# -------------------------
# MAIN RESPONSE FUNCTION (ADVANCED)
# -------------------------
def chatbot_response(user_input):
    text = user_input.lower()

    # Greeting
    if text in ["hi", "hello", "hey", "hii"]:
        return "Hello 👋! I'm your smart AI chatbot. Ask me anything!"

    # Thanks
    if "thank" in text:
        return "You're welcome 😊!"

    # Date & Time
    now = datetime.now(ist)
    if "time" in text and "date" not in text:
        return f"⏰ {now.strftime('%I:%M %p')}"

    if "date" in text and "time" not in text:
        return f"📅 {now.strftime('%d-%m-%Y')}"

    if "date" in text and "time" in text:
        return f"📅 {now.strftime('%d-%m-%Y')} | ⏰ {now.strftime('%I:%M %p')}"

    # Weather
    if "weather" in text:
        city = extract_city(user_input)
        if city == "":
            return "Please specify a city"
        return get_weather(city)

    # Festival (smart handling)
    fest = get_festival_info(user_input)
    if fest:
        return fest

    # Wikipedia (MAIN KNOWLEDGE ENGINE)
    wiki = get_wikipedia(user_input)
    if wiki:
        return wiki

    # Web fallback
    return search_web(user_input)

# -------------------------
# CHAT UI
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

    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            response = chatbot_response(user_input)

        if isinstance(response, list):
            st.markdown("### 🌐 Top Search Results")
            for res in response:
                st.markdown(f"**{res['title']}**\n{res.get('body','')}\n[Read more]({res['href']})")
                st.markdown("---")
        else:
            st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": str(response)})
