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
location = st.text_input("📍 Enter your location (address, city, or zip)")
time_of_day = st.selectbox("⏰ What time of day?", ["Morning", "Afternoon", "Evening", "Late Night"])
distance = st.slider("📏 Max travel distance (miles)", 1, 50, 10)

# Function to get lat/lon from location
def get_coordinates(location):
    API_KEY = os.getenv("GOOGLE_API_KEY")
    if not API_KEY:
        st.error("Google API Key not found.")
        return None, None

    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={API_KEY}"
    response = requests.get(url)
    try:
        data = response.json()
        if data["status"] == "OK":
            lat = data["results"][0]["geometry"]["location"]["lat"]
            lon = data["results"][0]["geometry"]["location"]["lng"]
            return lat, lon
        else:
            return None, None
    except Exception as e:
        st.error(f"Geocoding error: {e}")
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
    
def get_places(lat, lon, radius, keyword):
    import os
    API_KEY = os.getenv("GOOGLE_API_KEY")
    if not API_KEY:
        st.error("Google API Key not found. Please check your .env file.")
        return []

    # Convert miles to meters (Google requires meters)
    radius_meters = radius * 1609

    url = (
        f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
        f"location={lat},{lon}&radius={radius_meters}&keyword={keyword}"
        f"&opennow=true&key={API_KEY}"
    )

    response = requests.get(url)
    try:
        results = response.json().get("results", [])
        return results
    except:
        return []

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

    condition = classify_weather(temp, desc)

    # Map weather to place types
    weather_keywords = {
        "cold": "coffee|arcade|museum|indoor",
        "hot": "ice cream|lake|park|swimming",
        "rain": "cinema|museum|arcade|cafe",
        "mild": "outdoor|cafe|park|trail|picnic"
    }

    keyword = weather_keywords.get(condition, "date")

    # Fetch real places
    results = get_places(lat, lon, distance, keyword)

    if not results:
        st.warning("😕 No places found nearby that match the vibe.")
    else:
        for place in results[:5]:  # limit to 5 results
            name = place.get("name", "Unknown Place")
            address = place.get("vicinity", "Address not available")
            open_now = place.get("opening_hours", {}).get("open_now", None)
            rating = place.get("rating", "N/A")
            maps_url = f"https://www.google.com/maps/place/?q=place_id:{place['place_id']}"

            st.markdown(f"### 📍 [{name}]({maps_url})")
            st.markdown(f"- 📌 **Address:** {address}")
            st.markdown(f"- ⭐ **Rating:** {rating}")
            if open_now is not None:
                st.markdown(f"- 🟢 {'Open now' if open_now else 'Closed now'}")
            st.markdown("---")

