# langgraph_version/prompts.py
# Prompt templates for each graph node. The wording is lifted from the CrewAI
# task descriptions in crewai_version/tasks.py, with the agent role folded in
# as a system message and the upstream results passed in explicitly, since
# there is no manager agent to hand context around.
#
# Every template is formatted with str.format(**state_fields), so placeholders
# must match keys in TripDetails or GraphState.

SYSTEM_PROMPTS = {
    "research_deals": (
        "You are a Deal Finder. You find the best travel deals but only highlight "
        "the top value in minimal text."
    ),
    "generate_recommendations": (
        "You are a Recommendation Expert. You know global travel trends and "
        "personalize suggestions based on the user's past preferences: {user_preferences}"
    ),
    "plan_itinerary": (
        "You are a Travel Planner. You convert recommendations into a short "
        "day-by-day travel sketch."
    ),
    "generate_report": (
        "You are an Itinerary Finalizer. You wrap up all travel plans into an "
        "actionable summary with a total cost estimate."
    ),
    "validate_plan": (
        "You are the Travel Supervisor. You check the final plan and keep your "
        "answer minimal and high-level."
    ),
}

RESEARCH_DEALS = (
    "Find the cheapest flight and hotel deal from {origin} to {destination} "
    "for {num_travelers} between {start_date} and {end_date}.\n\n"
    "Web search results you can use:\n{search_results}\n\n"
    "Reply with just 1 hotel and 1 flight in under 2 lines, each with a price."
)

GENERATE_RECOMMENDATIONS = (
    "Based on the user's interests ({interests}) and travel style ({travel_style}), "
    "suggest one destination or activity tailored to their profile.\n\n"
    "Deals already found:\n{deals}\n\n"
    "Web search results you can use:\n{search_results}\n\n"
    "Keep the output minimal (1-2 lines only)."
)

PLAN_ITINERARY = (
    "Create a minimal 3-day itinerary for {destination}, covering meals, one main "
    "activity per day, and transport hints.\n\n"
    "Deals:\n{deals}\n\nRecommendation:\n{recommendations}\n\n"
    "Use bullet points, 3-4 lines only."
)

GENERATE_REPORT = (
    "Summarize the travel plan: destination, main activity, top deal, total budget "
    "(the user's budget is {budget_preference}).\n\n"
    "Deals:\n{deals}\n\nRecommendation:\n{recommendations}\n\n"
    "Itinerary:\n{itinerary}\n\n"
    "Keep it to 2-3 short lines, markdown format."
)

VALIDATE_PLAN = (
    "Review the content below and confirm if it is ready for the traveler.\n\n"
    "Original request:\n{natural_language_request}\n\n"
    "Report:\n{report}\n\n"
    "Respond with just one line: 'READY' or 'NEEDS EDIT: <reason>'."
)

# Search queries issued by the two research nodes.
DEALS_SEARCH_QUERY = "cheapest flights and hotels from {origin} to {destination} {start_date} {end_date}"
RECOMMENDATIONS_SEARCH_QUERY = "best {travel_style} travel destinations for {interests}"
