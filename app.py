import streamlit as st

# Agriculture database
agri_data = {
    "wheat": "Wheat is a major rabi crop in India. It is grown in Punjab, Haryana, and UP.",
    "rice": "Rice is a kharif crop. West Bengal is the largest producer.",
    "maize": "Maize is grown in Karnataka, Madhya Pradesh, and Bihar.",
    "fertilizer": "Fertilizers include urea, DAP, and potash.",
    "irrigation": "Irrigation methods include drip, sprinkler, and canals.",
    "soil": "India has alluvial, black, red, and laterite soils.",
    "organic farming": "Organic farming avoids chemicals and uses natural inputs.",
    "pesticides": "Pesticides protect crops but should be used in controlled amounts.",
    "msp": "Minimum Support Price is given by the government to farmers.",
    "kharif": "Kharif crops are sown in monsoon season.",
    "rabi": "Rabi crops are sown in winter season."
}

# Function to fetch response
def get_response(user_input):
    user_input = user_input.lower()
    
    for key in agri_data:
        if key in user_input:
            return agri_data[key]
    
    return "Sorry, I don't have information about that. Try asking about crops, soil, irrigation, etc."

# Streamlit UI
st.set_page_config(page_title="Agri Chatbot", page_icon="🌾")

st.title("🌾 Agriculture Chatbot (India)")
st.write("Ask me anything about Indian agriculture!")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input box
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
