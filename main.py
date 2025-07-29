# main.py
# Orchestrates the AI travel agent crew to generate a travel plan

import os
from dotenv import load_dotenv
from crewai import Crew, Process

# ✅ Load environment variables from .env file
env_file = "travelagent.env"
load_dotenv(dotenv_path=env_file)

# ✅ Import agents and tasks
from agents import deal_researcher, recommendation_agent, travel_planner, itinerary_generator, supervisor
from tasks import research_deals_task, generate_recommendations_task, plan_itinerary_task, generate_report_task, validate_plan_task

# ✅ This is the function you will call from FastAPI
def run_agentic_flow(trip_details: dict) -> dict:
    # Create the Crew
    project_crew = Crew(
        agents=[
            supervisor,
            recommendation_agent,
            deal_researcher,
            travel_planner,
            itinerary_generator
        ],
        tasks=[
            research_deals_task,
            generate_recommendations_task,
            plan_itinerary_task,
            generate_report_task,
            validate_plan_task
        ],
        process=Process.hierarchical,
        manager_llm=supervisor.llm,
        verbose=True
    )

    print("## Initiating Travel Planning Process...\n")
    result = project_crew.kickoff(inputs=trip_details)

    print("\n## Travel Planning Complete!")
    return {"result": result}


# ✅ Optional: Keep this for CLI testing
if __name__ == "__main__":
    # Demo request (used only if you run `python main.py` directly)
    travel_request = """
    I want to plan a fun and adventurous trip to Southeast Asia.
    I'm thinking of going sometime in November or December 2025 for about 10–14 days.
    My budget is around $2000–$3000, excluding flights.
    I love exploring vibrant cultures, trying local food, and engaging in outdoor activities like hiking or snorkeling.
    I'm traveling solo.
    """

    user_preferences = {
        "past_destinations": ["Thailand", "Vietnam", "Costa Rica"],
        "activity_types": ["hiking", "snorkeling", "cultural immersion", "food tours"],
        "travel_style": "adventurous",
        "budget_preference": "mid-range",
        "travel_companions": "solo",
        "dietary_restrictions": "vegetarian"
    }

    trip_details = {
        'origin': 'New York',
        'destination': 'Southeast Asia',
        'start_date': 'November 2025',
        'end_date': 'December 2025',
        'num_travelers': '1 (solo)',
        'budget_preference': '$2000-$3000 (excluding flights)',
        'interests': 'vibrant cultures, local food, hiking, snorkeling',
        'travel_style': 'adventurous',
        'natural_language_request': travel_request,
        'user_preferences': str(user_preferences)
    }

    # Run the agent directly for local testing
    result = run_agentic_flow(trip_details)
    print("Here's your comprehensive travel plan:\n")
    print(result["result"])
