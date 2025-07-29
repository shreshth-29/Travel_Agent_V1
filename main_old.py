# main.py
# Orchestrates the AI travel agent crew to generate a travel plan

import os
from dotenv import load_dotenv
from crewai import Crew, Process

# IMPORTANT: Load environment variables FIRST to ensure they are available for tool initialization.
env_file = "travelagent.env"
load_dotenv(dotenv_path=env_file)

# Import agents and tasks from their respective files.
# LLM initialization and assignment are now handled within agents.py.
from agents import deal_researcher, recommendation_agent, travel_planner, itinerary_generator, supervisor
from tasks import research_deals_task, generate_recommendations_task, plan_itinerary_task, generate_report_task, validate_plan_task

# User input for the travel demo.
# These details will be passed to the tasks for dynamic processing.
travel_request = """
I want to plan a fun and adventurous trip to Southeast Asia.
I'm thinking of going sometime in November or December 2025 for about 10-14 days.
My budget is around $2000-$3000, excluding flights.
I love exploring vibrant cultures, trying local food, and engaging in outdoor activities like hiking or snorkeling.
I'm traveling solo.
"""

# User preferences data - now defined in main.py
user_preferences = {
    "past_destinations": ["Thailand", "Vietnam", "Costa Rica"],
    "activity_types": ["hiking", "snorkeling", "cultural immersion", "food tours"],
    "travel_style": "adventurous",
    "budget_preference": "mid-range",
    "travel_companions": "solo",
    "dietary_restrictions": "vegetarian"
}

# Structured trip details - this will be passed as input to the crew
# Merged user_preferences into trip_details
trip_details = {
    'origin': 'New York', # Concrete origin for the demo
    'destination': 'Southeast Asia',
    'start_date': 'November 2025',
    'end_date': 'December 2025',
    'num_travelers': '1 (solo)',
    'budget_preference': '$2000-$3000 (excluding flights)',
    'interests': 'vibrant cultures, local food, hiking, snorkeling',
    'travel_style': 'adventurous',
    'natural_language_request': travel_request, # Include the original natural language request for agents to refer to
    'user_preferences': str(user_preferences) # Pass user_preferences as a string
}


# Create the Crew by assembling the agents and tasks.
# Using Process.hierarchical with the supervisor agent as the manager.
project_crew = Crew(
    agents=[
        supervisor, # Supervisor agent is now part of the crew
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
        validate_plan_task # Include the validation task
    ],
    process=Process.hierarchical, # Using hierarchical process for better coordination
    manager_llm=supervisor.llm, # Manager LLM is required for hierarchical process, using supervisor's LLM
    verbose=True
)

# Kick off the crew's work with the user's initial travel request
print("## Initiating Travel Planning Process...\n")
# Pass the structured trip_details directly to the kickoff method
result = project_crew.kickoff(inputs=trip_details)

print("\n## Travel Planning Complete!")
print("Here's your comprehensive travel plan:")
print(result)
