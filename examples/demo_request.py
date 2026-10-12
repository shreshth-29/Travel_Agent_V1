# examples/demo_request.py
# The demo trip request used by the CLI entry points. Edit freely.

TRAVEL_REQUEST = """
I want to plan a fun and adventurous trip to Southeast Asia.
I'm thinking of going sometime in November or December 2025 for about 10-14 days.
My budget is around $2000-$3000, excluding flights.
I love exploring vibrant cultures, trying local food, and engaging in outdoor activities like hiking or snorkeling.
I'm traveling solo.
"""

USER_PREFERENCES = {
    "past_destinations": ["Thailand", "Vietnam", "Costa Rica"],
    "activity_types": ["hiking", "snorkeling", "cultural immersion", "food tours"],
    "travel_style": "adventurous",
    "budget_preference": "mid-range",
    "travel_companions": "solo",
    "dietary_restrictions": "vegetarian",
}

DEMO_TRIP_DETAILS = {
    "origin": "New York",
    "destination": "Southeast Asia",
    "start_date": "November 2025",
    "end_date": "December 2025",
    "num_travelers": "1 (solo)",
    "budget_preference": "$2000-$3000 (excluding flights)",
    "interests": "vibrant cultures, local food, hiking, snorkeling",
    "travel_style": "adventurous",
    "natural_language_request": TRAVEL_REQUEST,
    "user_preferences": str(USER_PREFERENCES),
}
