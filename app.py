from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("OWM_API_KEY")
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


def get_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=imperial&appid={API_KEY}"
    response = requests.get(url)
    try:
        data = response.json()
        if response.status_code == 200:
            temp = data['main']['temp']
            desc = data['weather'][0]['description'].title()
            return temp, desc
        else:
            return None, None
    except:
        return None, None

def classify_weather(temp, desc):
    condition = "mild"
    if temp < 40:
        condition = "cold"
    elif temp > 85:
        condition = "hot"
    if "rain" in desc.lower() or "storm" in desc.lower():
        condition = "rain"
    return condition


# Output section
if st.button("🎯 Get Date Ideas"):
    lat, lon = get_coordinates(location)
    temp, desc = get_weather(lat, lon)

    if temp is not None:
        st.info(f"🌡️ Weather in {location}: {temp:.0f}°F, {desc}")
    else:
        st.warning("⚠️ Couldn't get weather data.")

    if lat is None:
        st.error("❌ Couldn't find that location. Please try a different city or zip.")
        st.stop()
    else:
        st.success(f"📍 Coordinates found: {lat:.2f}, {lon:.2f}")

    st.subheader("Here are 3 ideas:")

    condition = classify_weather(temp, desc)

    ideas = []

    if condition == "cold":
        ideas = [
            {
                "title": "Cozy Cafe Hop",
                "location": "Downtown coffee spots",
                "note": "Stay warm while taste-testing local drinks."
            },
            {
                "title": "Board Game Lounge",
                "location": "Indoor game bar or library",
                "note": "Team up or go head-to-head inside where it's warm."
            },
        ]
    elif condition == "hot":
        ideas = [
            {
                "title": "Lake Day & Ice Cream",
                "location": "Nearest public beach",
                "note": "Swim, tan, and cool off with a cone."
            },
            {
                "title": "Sunset Rooftop Drinks",
                "location": "Open-air rooftop bar",
                "note": "Chill vibes and cold beverages as the sun sets."
            },
        ]
    elif condition == "rain":
        ideas = [
            {
                "title": "Rainy Movie Marathon",
                "location": "Home or boutique cinema",
                "note": "Cuddle up with a classic or something new."
            },
            {
                "title": "Indoor Mini Golf",
                "location": "Glow-in-the-dark golf lounge",
                "note": "Fun, competitive, and rainproof."
            },
        ]
    else:  # mild weather
        ideas = [
            {
                "title": "Scenic Park Picnic",
                "location": "Local botanical garden or park",
                "note": "Relax, eat, and enjoy the fresh air."
            },
            {
                "title": "Farmers Market Adventure",
                "location": "Outdoor local market",
                "note": "Pick snacks or flowers together."
            },
        ]


    for idea in ideas:
        st.markdown(f"### 📝 {idea['title']}")
        st.markdown(f"📍 **Location**: {idea['location']}")
        st.markdown(f"💡 {idea['note']}")
        st.markdown("---")
