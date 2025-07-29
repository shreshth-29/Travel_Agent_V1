# streamlit_app.py
import streamlit as st
import requests
import json

st.set_page_config(page_title="Agentic Travel Planner")

st.title("🌍 Agentic AI Travel Planner")

st.markdown("Fill in your preferences and click **Plan My Trip** to generate a personalized itinerary.")

# --- Form inputs ---
with st.form("trip_form"):
    origin = st.text_input("Origin", "New York")
    destination = st.text_input("Destination", "Southeast Asia")
    start_date = st.text_input("Start Date", "November 2025")
    end_date = st.text_input("End Date", "December 2025")
    num_travelers = st.text_input("Number of Travelers", "1 (solo)")
    budget = st.text_input("Budget", "$2000-$3000 (excluding flights)")
    travel_style = st.selectbox("Travel Style", ["adventurous", "relaxed", "luxury"])
    interests = st.text_area("Interests", "vibrant cultures, local food, hiking, snorkeling")
    dietary = st.text_input("Dietary Restrictions", "vegetarian")
    natural_language_request = st.text_area("Your Request", "I want to plan a fun and adventurous trip to Southeast Asia...")

    submitted = st.form_submit_button("Plan My Trip")

if submitted:
    with st.spinner("Planning your adventure... ⏳"):
        # Construct payload
        trip_details = {
            "origin": origin,
            "destination": destination,
            "start_date": start_date,
            "end_date": end_date,
            "num_travelers": num_travelers,
            "budget_preference": budget,
            "interests": interests,
            "travel_style": travel_style,
            "natural_language_request": natural_language_request,
            "user_preferences": str({
                "travel_style": travel_style,
                "activity_types": interests.split(", "),
                "budget_preference": budget,
                "travel_companions": num_travelers,
                "dietary_restrictions": dietary
            })
        }

        try:
            response = requests.post(
                "http://localhost:8000/plan-trip",  # or your deployed FastAPI URL
                json={"trip_details": trip_details}
            )
            data = response.json()
            st.success("Trip successfully planned!")
            st.markdown("---")
            st.markdown(data["result"])  # assuming output is markdown
        except Exception as e:
            st.error(f"Something went wrong: {e}")
