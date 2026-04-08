import streamlit as st
from datetime import datetime
import pytz
import requests
import wikipedia
from duckduckgo_search import DDGS

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
    return " ".join(city_words).strip()

# -------------------------
# WEATHER: GET COORDINATES
# -------------------------
def get_coordinates(city):
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&country=India"
        data = requests.get(url).json()
        return data["results"][0]["latitude"], data["results"][0]["longitude"]
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
# WIKIPEDIA SMART
# -------------------------
def extract_keywords(query):
    stopwords = ["what","is","the","of","in","on","tell","me","about","who","was","are","were","when"]
    words = query.lower().split()
    keywords = [word for word in words if word not in stopwords]
    return " ".join(keywords)

def get_wikipedia(query):
    try:
        keywords = extract_keywords(query)
        results = wikipedia.search(keywords)

        if not results:
            return "❌ No relevant information found."

        page = wikipedia.page(results[0])
        paragraphs = page.content.split("\n")

        for para in paragraphs:
            if any(word in para.lower() for word in keywords.split()):
                if len(para) > 100:
                    return f"📚 {para[:400]}..."

        return f"📚 {wikipedia.summary(results[0], sentences=2)}"

    except wikipedia.exceptions.DisambiguationError as e:
        return f"⚠️ Be more specific. Options: {', '.join(e.options[:5])}"
    except:
        return "❌ Unable to fetch information."

# -------------------------
# 🌐 SEARCH FUNCTION (UI READY)
# -------------------------
def search_web(query):
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=5):
                results.append(r)

        return results if results else "❌ No results found."
    except:
        return "⚠️ Search not working."

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

    # Weather
    if "weather" in text:
        city = extract_city(user_input)
        if city == "":
            return "Please specify a city. Example: weather in Delhi"
        return get_weather(city)

    # Web Search
    if "search" in text or "google" in text:
        query = user_input.replace("search", "").replace("google", "")
        return search_web(query)

    # Wikipedia fallback
    return get_wikipedia(user_input)

# -------------------------
# CHAT UI
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat
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

        # 🌐 Premium Search UI
        if isinstance(response, list):
            st.markdown("### 🌐 Top Search Results")

            for res in response:
                st.markdown(f"""
                🔹 **{res['title']}**  
                {res.get('body', '')}  
                [Read more]({res['href']})
                """)
                st.markdown("---")

        else:
            st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": str(response)})
