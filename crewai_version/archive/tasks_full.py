# crewai_version/archive/tasks_full.py
# The original long-form task definitions that produced the sample outputs in
# examples/. Not imported by the live code.

from crewai import Task

from crewai_version.archive.agents_full import (
    deal_researcher,
    itinerary_generator,
    recommendation_agent,
    supervisor,
    travel_planner,
)

research_deals_task = Task(
    description=(
        "Research the best flight and hotel deals for a trip from {origin} to {destination} "
        "from {start_date} to {end_date} for {num_travelers} travelers. "
        "Focus on finding options within a {budget_preference} budget. "
        "Provide direct links if possible and summarize key details. "
        "The user's original request was: {natural_language_request}"
    ),
    expected_output=(
        "A markdown formatted list of top 3 flight options (airline, price, dates) and top 3 "
        "hotel options (name, price per night, rating, location) with brief justifications for each."
    ),
    agent=deal_researcher,
)

generate_recommendations_task = Task(
    description=(
        "Based on the researched deals and the user's interests ({interests}) and travel style "
        "({travel_style}), generate personalized travel recommendations. "
        "Consider simulating past user preferences/history (e.g., a preference for boutique hotels, "
        "or specific types of activities like museums or outdoor adventures) to make the "
        "recommendations highly relevant. "
        "Provide suggestions for unique experiences or hidden gems not explicitly covered in the itinerary. "
        "The user's original request was: {natural_language_request}"
    ),
    expected_output=(
        "A markdown formatted list of personalized recommendations, including unique experiences, "
        "dining suggestions, or activities, justified by user preferences."
    ),
    agent=recommendation_agent,
)

plan_itinerary_task = Task(
    description=(
        "Create a detailed, day-by-day travel itinerary for {destination} from {start_date} to {end_date} "
        "for {num_travelers} travelers, based on the researched deals and generated recommendations. "
        "Include daily activities, suggested dining, and transportation options. "
        "Consider {interests} and {travel_style}. "
        "The user's original request was: {natural_language_request}"
    ),
    expected_output=(
        "A comprehensive markdown formatted daily itinerary, including specific times, venues, "
        "and estimated costs for each activity and meal."
    ),
    agent=travel_planner,
)

generate_report_task = Task(
    description=(
        "Compile the researched deals, personalized recommendations, and the detailed itinerary into "
        "a final, polished travel report. Ensure the report is well-structured, easy to read, and "
        "includes all essential information like flight/hotel summaries, daily itinerary, overall "
        "budget considerations, and unique recommendations. The report should be suitable for a traveler. "
        "The user's original request was: {natural_language_request}"
    ),
    expected_output="A complete, engaging travel report in markdown format, ready to be presented to the traveler.",
    agent=itinerary_generator,
)

validate_plan_task = Task(
    description=(
        "Review the generated travel report for completeness, accuracy, and adherence to user preferences. "
        "Ensure all requested information is present and the tone is helpful and professional. "
        "The user's original request was: {natural_language_request}"
    ),
    expected_output="A confirmation that the travel report is ready, or specific feedback for improvements.",
    agent=supervisor,
)
