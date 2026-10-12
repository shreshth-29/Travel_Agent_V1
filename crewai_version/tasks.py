# crewai_version/tasks.py
# Task definitions for the CrewAI backend. Placeholders in braces are filled
# from the trip_details dict passed to Crew.kickoff(inputs=...).

from crewai import Task

from crewai_version.agents import (
    deal_researcher,
    itinerary_generator,
    recommendation_agent,
    supervisor,
    travel_planner,
)

research_deals_task = Task(
    description=(
        "Find the cheapest flight and hotel deal from {origin} to {destination} "
        "for {num_travelers} between {start_date} and {end_date}. "
        "Reply with just 1 hotel and 1 flight in under 2 lines."
    ),
    expected_output="Top flight and hotel deal in 2 short lines with price.",
    agent=deal_researcher,
)

generate_recommendations_task = Task(
    description=(
        "Based on the user's interests ({interests}) and travel style ({travel_style}), "
        "suggest one destination or activity tailored to their profile. "
        "Keep the output minimal (1-2 lines only)."
    ),
    expected_output="One-liner destination/activity suggestion.",
    agent=recommendation_agent,
)

plan_itinerary_task = Task(
    description=(
        "Create a minimal 3-day itinerary for {destination}, covering meals, one main activity per day, "
        "and transport hints. Use bullet points, 3-4 lines only."
    ),
    expected_output="Compact 3-day bullet itinerary (max 4 lines).",
    agent=travel_planner,
)

generate_report_task = Task(
    description=(
        "Summarize the travel plan: destination, main activity, top deal, total budget. "
        "Keep it to 2-3 short lines, markdown format."
    ),
    expected_output="2-3 line trip report summary with total estimate.",
    agent=itinerary_generator,
)

validate_plan_task = Task(
    description=(
        "Review the above content and confirm if it's ready. Respond with just one line: "
        "'READY' or 'NEEDS EDIT: <reason>'."
    ),
    expected_output="Single line status.",
    agent=supervisor,
)
