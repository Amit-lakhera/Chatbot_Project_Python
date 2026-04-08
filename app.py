import streamlit as st
from datetime import datetime
import pytz
import requests
import wikipedia

st.set_page_config(page_title="Smart AI Chatbot", page_icon="🤖")
st.title("🤖 Smart AI Chatbot")

# IST Timezone
ist = pytz.timezone("Asia/Kolkata")

# -------------------------
# WEATHER: EXTRACT CITY
# -------------------------
def extract_city(user_input):
    text = user_input.lower()

    remove_words = ["weather", "in", "of", "what", "is", "the", "tell", "me"]
    words = text.split()

    city_words = [word for word in words if word not in remove_words]
    city = " ".join(city_words)

    return city.strip()

# -------------------------
# WEATHER: GET COORDINATES
# -------------------------
def get_coordinates(city):
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&country=India"
        data = requests.get(url).json()

        lat = data["results"][0]["latitude"]
        lon = data["results"][0]["longitude"]

        return lat, lon
    except:
        return None, None

# -------------------------
# WEATHER FUNCTION
# -------------------------
def get_weather(city):
    lat, lon = get_coordinates(city)

    if lat is None:
        return "❌ Location not found. Try a valid Indian city."

    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        data = requests.get(url).json()

        temp = data["current_weather"]["temperature"]
        wind = data["current_weather"]["windspeed"]

        return f"🌦️ Weather in {city.title()}:\nTemperature: {temp}°C\nWind Speed: {wind} km/h"
    except:
        return "⚠️ Unable to fetch weather."

# -------------------------
# WIKIPEDIA: KEYWORD EXTRACTION
# -------------------------
def extract_keywords(query):
    stopwords = [
        "what", "is", "the", "of", "in", "on", "tell", "me",
        "about", "who", "was", "are", "were", "when"
    ]

    words = query.lower().split()
    keywords = [word for word in words if word not in stopwords]

    return " ".join(keywords)

# -------------------------
# SMART WIKIPEDIA FUNCTION
# -------------------------
def get_wikipedia(query):
    try:
        keywords = extract_keywords(query)

        search_results = wikipedia.search(keywords)

        if not search_results:
            return "❌ No relevant information found."

        page = wikipedia.page(search_results[0])
        content = page.content

        paragraphs = content.split("\n")

        # Find relevant paragraph
        for para in paragraphs:
            if any(word in para.lower() for word in keywords.split()):
                if len(para) > 100:
                    return f"📚 {para[:400]}..."

        # fallback
        return f"📚 {wikipedia.summary(search_results[0], sentences=2)}"

    except wikipedia.exceptions.DisambiguationError as e:
        return f"⚠️ Be more specific. Options: {', '.join(e.options[:5])}"

    except wikipedia.exceptions.PageError:
        return "❌ Page not found. Try another query."

    except:
        return "❌ Unable to fetch information right now."

# -------------------------
# MAIN RESPONSE FUNCTION
# -------------------------
def chatbot_response(user_input):
    text = user_input.lower()

    # Greeting
    if text in ["hi", "hello", "hey", "hii"]:
        return "Hello 👋! I'm your smart AI chatbot. Ask me about weather, date, time or anything!"

    # Thanks
    if "thank" in text:
        return "You're welcome 😊! Happy to help!"

    # Date & Time (IST)
    now = datetime.now(ist)
    current_time = now.strftime("%I:%M %p")
    current_date = now.strftime("%d-%m-%Y")

    if "time" in text and "date" not in text:
        return f"⏰ Current Time (IST): {current_time}"

    if "date" in text and "time" not in text:
        return f"📅 Today's Date: {current_date}"

    if "date" in text and "time" in text:
        return f"📅 Date: {current_date}\n⏰ Time (IST): {current_time}"

    # Weather
    if "weather" in text:
        city = extract_city(user_input)

        if city == "":
            return "Please specify a city. Example: weather in Delhi"

        return get_weather(city)

    # Wikipedia fallback (smart)
    return get_wikipedia(user_input)

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

    response = chatbot_response(user_input)

    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
