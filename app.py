import streamlit as st
from datetime import datetime, timedelta
import pytz
import requests
import wikipedia
from duckduckgo_search import DDGS

st.set_page_config(page_title="Smart AI Chatbot", page_icon="🤖")
st.title("🤖 Smart AI Chatbot with Indian Calendar")

# IST Timezone
ist = pytz.timezone("Asia/Kolkata")

# -------------------------
# 🇮🇳 INDIAN FESTIVALS (EXTENDED)
# -------------------------
indian_festivals = {
    2025: {
        "diwali": "21 October 2025",
        "holi": "14 March 2025",
        "eid": "31 March 2025",
        "raksha bandhan": "9 August 2025",
        "dussehra": "2 October 2025",
        "janmashtami": "16 August 2025",
        "pongal": "14 January 2025",
        "baisakhi": "13 April 2025",
        "navratri": "22 September 2025"
    },
    2026: {
        "diwali": "8 November 2026",
        "holi": "3 March 2026",
        "eid": "20 March 2026",
        "raksha bandhan": "28 August 2026",
        "dussehra": "20 October 2026",
        "janmashtami": "5 September 2026",
        "pongal": "14 January 2026",
        "baisakhi": "13 April 2026",
        "navratri": "11 October 2026"
    }
}

# -------------------------
# 📅 FESTIVAL FUNCTION
# -------------------------
def get_festival_date(user_input):
    text = user_input.lower()
    year = datetime.now().year

    for y in indian_festivals:
        if str(y) in text:
            year = y

    for fest in indian_festivals.get(year, {}):
        if fest in text:
            return f"🎉 {fest.title()} in {year} is on {indian_festivals[year][fest]}"

    if "festival" in text:
        data = indian_festivals.get(year, {})
        return "\n".join([f"• {k.title()} → {v}" for k, v in data.items()])

    return None

# -------------------------
# 🗓️ CALENDAR UI
# -------------------------
def show_calendar():
    st.subheader("📅 Indian Festival Calendar")
    year = st.selectbox("Select Year", list(indian_festivals.keys()))

    for fest, date in indian_festivals[year].items():
        st.write(f"🎉 {fest.title()} → {date}")

# -------------------------
# WEATHER
# -------------------------
def extract_city(user_input):
    text = user_input.lower()
    remove_words = ["weather", "in", "of", "what", "is", "the"]
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
        return "❌ City not found"

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    data = requests.get(url).json()

    temp = data["current_weather"]["temperature"]
    wind = data["current_weather"]["windspeed"]
    return f"🌦️ Weather in {city.title()}: {temp}°C, Wind {wind} km/h"

# -------------------------
# WIKIPEDIA
# -------------------------
def get_wikipedia(query):
    try:
        return wikipedia.summary(query, sentences=3)
    except:
        return "❌"

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
        return "⚠️"

# -------------------------
# MAIN RESPONSE FUNCTION
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
    current_time = now.strftime("%I:%M %p")
    current_date = now.strftime("%d-%m-%Y")

    if "time" in text and "date" not in text:
        return f"⏰ Time (IST): {current_time}"

    if "date" in text and "time" not in text:
        return f"📅 Date: {current_date}"

    if "date" in text and "time" in text:
        return f"📅 Date: {current_date}\n⏰ Time: {current_time}"

    # Festival
    fest = get_festival_date(user_input)
    if fest:
        return fest

    # Weather
    if "weather" in text:
        city = extract_city(user_input)
        if city == "":
            return "Please specify a city. Example: weather in Delhi"
        return get_weather(city)

    # Wikipedia
    wiki_result = get_wikipedia(user_input)
    if wiki_result not in ["❌", "⚠️"]:
        return wiki_result

    # Web search fallback
    return search_web(user_input)

# -------------------------
# CHAT UI
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):

        with st.spinner("🤔 Thinking..."):
            response = chatbot_response(user_input)

        # 🌐 Search UI
        if isinstance(response, list):
            st.markdown("### 🌐 Top Search Results")
            st.info("🔍 Searching the web...")

            for res in response:
                st.markdown(f"""
                🔹 **{res['title']}**  
                {res.get('body', '')}  
                [Read more]({res['href']})
                """)
                st.markdown("---")

        else:
            st.success("✅ Answer found")
            st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": str(response)})

# Calendar UI removed (can be added later via a button if needed)
# if st.button("Show Festival Calendar"):
#     show_calendar()
