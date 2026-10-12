# streamlit_app.py
# Streamlit front end. Run with: streamlit run streamlit_app.py
#
# By default it calls the FastAPI server at API_URL (http://localhost:8000).
# Set CALL_BACKEND_DIRECTLY=1 to run the agent in-process instead, which is
# handy when you do not want to start uvicorn. In both cases the backend is
# selected by AGENT_BACKEND, and can be overridden in the sidebar.

import os

import requests
import streamlit as st

from settings import BACKENDS, get_backend, load_env

load_env()

API_URL = os.getenv("API_URL", "http://localhost:8000")
CALL_BACKEND_DIRECTLY = os.getenv("CALL_BACKEND_DIRECTLY", "0") == "1"

st.set_page_config(page_title="Agentic Travel Planner")
st.title("Agentic AI Travel Planner")
st.markdown("Fill in your preferences and click **Plan My Trip** to generate a personalized itinerary.")

with st.sidebar:
    backend = st.selectbox("Backend", BACKENDS, index=BACKENDS.index(get_backend()))
    st.caption(
        "Calling the agent in-process" if CALL_BACKEND_DIRECTLY else f"Calling the API at {API_URL}"
    )

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
    natural_language_request = st.text_area(
        "Your Request", "I want to plan a fun and adventurous trip to Southeast Asia..."
    )
    submitted = st.form_submit_button("Plan My Trip")

if submitted:
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
        "user_preferences": str(
            {
                "travel_style": travel_style,
                "activity_types": interests.split(", "),
                "budget_preference": budget,
                "travel_companions": num_travelers,
                "dietary_restrictions": dietary,
            }
        ),
    }

    with st.spinner(f"Planning your trip with the {backend} backend..."):
        try:
            if CALL_BACKEND_DIRECTLY:
                from settings import get_runner

                data = get_runner(backend)(trip_details)
            else:
                response = requests.post(
                    f"{API_URL}/plan-trip",
                    json={"trip_details": trip_details, "backend": backend},
                    timeout=600,
                )
                response.raise_for_status()
                data = response.json()
            st.success("Trip planned.")
            st.markdown("---")
            st.markdown(data["result"])
        except Exception as e:
            st.error(f"Something went wrong: {e}")
