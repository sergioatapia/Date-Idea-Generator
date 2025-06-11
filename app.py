import requests
import streamlit as st
from datetime import datetime

# App layout
st.set_page_config(page_title="Date Idea Generator", page_icon="❤️", layout="centered")
st.title("💘 Date Idea Generator")
st.markdown("Get fun date ideas based on your time, location, and vibe.")

# Input fields
location = st.text_input("📍 Enter your city or zip code")
time_of_day = st.selectbox("⏰ What time of day?", ["Morning", "Afternoon", "Evening", "Late Night"])
distance = st.slider("📏 Max travel distance (miles)", 1, 50, 10)

# Your OpenWeather API key
API_KEY = "4664a3ab742d77aaef2535be50aeba32"

# Function to get lat/lon from location
def get_coordinates(location):
    if not location:
        return None, None

    # Determine if input looks like a ZIP code (all digits)
    if location.strip().isdigit():
        url = f"http://api.openweathermap.org/geo/1.0/zip?zip={location},US&appid={API_KEY}"
    else:
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={API_KEY}"

    response = requests.get(url)
    try:
        data = response.json()
        if isinstance(data, list) and data:
            return data[0]['lat'], data[0]['lon']
        elif isinstance(data, dict) and 'lat' in data:
            return data['lat'], data['lon']
        else:
            return None, None
    except Exception as e:
        st.error(f"API Error: {e}")
        return None, None




# Output section
if st.button("🎯 Get Date Ideas"):
    lat, lon = get_coordinates(location)

    if lat is None:
        st.error("❌ Couldn't find that location. Please try a different city or zip.")
        st.stop()
    else:
        st.success(f"📍 Coordinates found: {lat:.2f}, {lon:.2f}")

    st.subheader("Here are 3 ideas:")

    ideas = [
        {
            "title": "Sunrise Coffee & Walk",
            "location": "Local lake or trail",
            "note": "Start the day with fresh air and good conversation."
        },
        {
            "title": "Arcade + Pizza Combo",
            "location": "Nearest retro barcade",
            "note": "Play games, grab a slice, and laugh together."
        },
        {
            "title": "Stargazing Escape",
            "location": f"Scenic lookout ~{distance} mi from {location}",
            "note": "Blanket, snacks, and the stars."
        }
    ]

    for idea in ideas:
        st.markdown(f"### 📝 {idea['title']}")
        st.markdown(f"📍 **Location**: {idea['location']}")
        st.markdown(f"💡 {idea['note']}")
        st.markdown("---")
