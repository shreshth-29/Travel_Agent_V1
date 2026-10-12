# crewai_version/archive/agents_full.py
# The original long-form agent definitions. The sample outputs in examples/
# were produced with these and the matching tasks in tasks_full.py, before the
# prompts were shortened for faster testing. Not imported by the live code.

import os

from crewai import Agent
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from langchain_google_genai import ChatGoogleGenerativeAI

serper_tool = SerperDevTool()
scrape_website_tool = ScrapeWebsiteTool()

gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)

supervisor = Agent(
    role="Travel Planning Supervisor",
    goal=(
        "Oversee the entire travel planning process, ensuring all agents work collaboratively "
        "to deliver a comprehensive and personalized travel plan that meets the user's request."
    ),
    backstory=(
        "An experienced project manager in AI-driven travel solutions, skilled at delegating "
        "tasks, monitoring progress, and ensuring high-quality, cohesive outputs from a team of "
        "specialized AI agents."
    ),
    verbose=True,
    allow_delegation=True,
    llm=gemini_llm,
)

recommendation_agent = Agent(
    role="Travel Recommendation Expert",
    goal=(
        "Based on user preferences and historical data, recommend suitable destinations and "
        "activities that align with their adventurous travel style, budget, and interests."
    ),
    backstory=(
        "A seasoned travel consultant with a deep understanding of global destinations and "
        "adventure activities. Specializes in matching unique experiences to individual traveler "
        "profiles. Leverages past user preferences: {user_preferences}."
    ),
    tools=[serper_tool],
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm,
)

deal_researcher = Agent(
    role="Travel Deal Researcher",
    goal=(
        "Find the best flight, accommodation, and activity deals for the specified travel "
        "criteria and budget, ensuring value for money."
    ),
    backstory=(
        "A meticulous financial analyst specialized in travel, constantly scanning the web "
        "for the most cost-effective and high-value travel opportunities. "
        "Uses advanced search and scraping tools to unearth hidden gems and discounts."
    ),
    tools=[serper_tool, scrape_website_tool],
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm,
)

travel_planner = Agent(
    role="Comprehensive Travel Planner",
    goal=(
        "Synthesize recommendations and deal research into a coherent, detailed travel plan "
        "including logistics, budget breakdown, and practical advice."
    ),
    backstory=(
        "An expert in logistics and travel itinerary creation, known for transforming raw "
        "data into actionable, well-structured travel blueprints. Ensures every detail, "
        "from transport to local customs, is covered."
    ),
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm,
)

itinerary_generator = Agent(
    role="Detailed Itinerary Creator",
    goal=(
        "Generate a day-by-day itinerary based on the comprehensive travel plan, "
        "including specific activities, timings, and local tips."
    ),
    backstory=(
        "A creative and organized itinerary specialist who crafts engaging and realistic "
        "daily schedules, ensuring a smooth and enjoyable travel experience. "
        "Provides practical tips for each day."
    ),
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm,
)
