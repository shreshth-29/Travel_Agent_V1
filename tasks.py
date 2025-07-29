# tasks.py
# Define the tasks for the AI travel agent crew

from crewai import Task
from agents import deal_researcher, recommendation_agent, travel_planner, itinerary_generator, supervisor

# Task for the Deal Researcher: Research flight and hotel deals.
research_deals_task = Task(
    description=(
        "Research the best flight and hotel deals for a trip from {origin} to {destination} "
        "from {start_date} to {end_date} for {num_travelers} travelers. "
        "Focus on finding options within a {budget_preference} budget."
        "Provide direct links if possible and summarize key details."
        "The user's original request was: {natural_language_request}"
    ),
    expected_output='A markdown formatted list of top 3 flight options (airline, price, dates) and top 3 hotel options (name, price per night, rating, location) with brief justifications for each.',
    agent=deal_researcher # Assign this task to the deal_researcher agent
)

# Task for the Recommendation Agent: Generate personalized recommendations.
generate_recommendations_task = Task(
    description=(
        "Based on the researched deals and the user's interests ({interests}) and travel style ({travel_style}), "
        "generate personalized travel recommendations. "
        "Consider simulating past user preferences/history (e.g., a preference for boutique hotels, or specific types of activities like museums or outdoor adventures) "
        "to make the recommendations highly relevant. "
        "Provide suggestions for unique experiences or hidden gems not explicitly covered in the itinerary."
        "The user's original request was: {natural_language_request}"
    ),
    expected_output='A markdown formatted list of personalized recommendations, including unique experiences, dining suggestions, or activities, justified by user preferences.',
    agent=recommendation_agent # Assign this task to the recommendation_agent
)

# Task for the Travel Planner: Create a detailed itinerary.
plan_itinerary_task = Task(
    description=(
        "Create a detailed, day-by-day travel itinerary for {destination} from {start_date} to {end_date} "
        "for {num_travelers} travelers, based on the researched deals and generated recommendations. "
        "Include daily activities, suggested dining, and transportation options. "
        "Consider {interests} and {travel_style}."
        "The user's original request was: {natural_language_request}"
    ),
    expected_output='A comprehensive markdown formatted daily itinerary, including specific times, venues, and estimated costs for each activity and meal.',
    agent=travel_planner # Assign this task to the travel_planner agent
)

# Task for the Itinerary Generator: Compile the final travel report.
generate_report_task = Task(
    description=(
        "Compile the researched deals, personalized recommendations, and the detailed itinerary into a final, polished travel report. "
        "Ensure the report is well-structured, easy to read, and includes all essential information "
        "like flight/hotel summaries, daily itinerary, overall budget considerations, and unique recommendations. "
        "The report should be suitable for a traveler."
        "The user's original request was: {natural_language_request}"
    ),
    expected_output='A complete, engaging travel report in markdown format, ready to be presented to the traveler.',
    agent=itinerary_generator # Assign this task to the itinerary_generator agent
)

# Task for the Supervisor: Validate the final plan.
# This task is particularly useful in a hierarchical process for quality assurance.
validate_plan_task = Task(
    description=(
        "Review the generated travel report for completeness, accuracy, and adherence to user preferences. "
        "Ensure all requested information is present and the tone is helpful and professional."
        "The user's original request was: {natural_language_request}"
    ),
    expected_output='A confirmation that the travel report is ready, or specific feedback for improvements.',
    agent=supervisor # Assign this task to the supervisor agent
)





























# # tasks.py
# # Define the tasks for the AI travel agent crew

# from crewai import Task
# from agents import deal_researcher, recommendation_agent, travel_planner, itinerary_generator, supervisor

# # Task for the Deal Researcher: Research flight and hotel deals.
# research_deals_task = Task(
#     description=(
#         "Research the best flight and hotel deals for a trip from {origin} to {destination} "
#         "from {start_date} to {end_date} for {num_travelers} travelers. "
#         "Focus on finding options within a {budget_preference} budget."
#         "Provide direct links if possible and summarize key details."
#     ),
#     expected_output='A markdown formatted list of top 3 flight options (airline, price, dates) and top 3 hotel options (name, price per night, rating, location) with brief justifications for each.',
#     agent=deal_researcher # Assign this task to the deal_researcher agent
# )

# # Task for the Recommendation Agent: Generate personalized recommendations.
# generate_recommendations_task = Task(
#     description=(
#         "Based on the researched deals and the user's interests ({interests}) and travel style ({travel_style}), "
#         "generate personalized travel recommendations. "
#         "Consider simulating past user preferences/history (e.g., a preference for boutique hotels, or specific types of activities like museums or outdoor adventures) "
#         "to make the recommendations highly relevant. "
#         "Provide suggestions for unique experiences or hidden gems not explicitly covered in the itinerary."
#     ),
#     expected_output='A markdown formatted list of personalized recommendations, including unique experiences, dining suggestions, or activities, justified by user preferences.',
#     agent=recommendation_agent # Assign this task to the recommendation_agent
# )

# # Task for the Travel Planner: Create a detailed itinerary.
# plan_itinerary_task = Task(
#     description=(
#         "Create a detailed, day-by-day travel itinerary for {destination} from {start_date} to {end_date} "
#         "for {num_travelers} travelers, based on the researched deals and generated recommendations. "
#         "Include daily activities, suggested dining, and transportation options. "
#         "Consider {interests} and {travel_style}."
#     ),
#     expected_output='A comprehensive markdown formatted daily itinerary, including specific times, venues, and estimated costs for each activity and meal.',
#     agent=travel_planner # Assign this task to the travel_planner agent
# )

# # Task for the Itinerary Generator: Compile the final travel report.
# generate_report_task = Task(
#     description=(
#         "Compile the researched deals, personalized recommendations, and the detailed itinerary into a final, polished travel report. "
#         "Ensure the report is well-structured, easy to read, and includes all essential information "
#         "like flight/hotel summaries, daily itinerary, overall budget considerations, and unique recommendations. "
#         "The report should be suitable for a traveler."
#     ),
#     expected_output='A complete, engaging travel report in markdown format, ready to be presented to the traveler.',
#     agent=itinerary_generator # Assign this task to the itinerary_generator agent
# )

# # Task for the Supervisor: Validate the final plan.
# # This task is particularly useful in a hierarchical process for quality assurance.
# validate_plan_task = Task(
#     description=(
#         "Review the generated travel report for completeness, accuracy, and adherence to user preferences. "
#         "Ensure all requested information is present and the tone is helpful and professional."
#     ),
#     expected_output='A confirmation that the travel report is ready, or specific feedback for improvements.',
#     agent=supervisor # Assign this task to the supervisor agent
# )