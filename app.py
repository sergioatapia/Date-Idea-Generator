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

# Output section
if st.button("🎯 Get Date Ideas"):
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
