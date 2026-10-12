# crewai_version/agents.py
# Agent definitions for the CrewAI backend.
#
# All agents share one Gemini model. The output token cap is deliberately low
# so that the crew returns compact answers; raise MAX_OUTPUT_TOKENS in the
# environment to get longer reports (see archive/ for the original long-form
# agent and task definitions).

import os

from crewai import Agent
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from langchain_google_genai import ChatGoogleGenerativeAI

gemini_llm = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    max_output_tokens=int(os.getenv("MAX_OUTPUT_TOKENS", "256")),
    temperature=0.7,
)

# Tools. SerperDevTool reads SERPER_API_KEY from the environment.
serper_tool = SerperDevTool()
scrape_website_tool = ScrapeWebsiteTool()

supervisor = Agent(
    role="Travel Supervisor",
    goal="Summarize and validate the trip plan in 1-2 lines.",
    backstory="Manages the overall output but keeps it minimal and high-level.",
    allow_delegation=True,
    verbose=True,
    llm=gemini_llm,
)

recommendation_agent = Agent(
    role="Recommendation Expert",
    goal="Suggest one destination or activity tailored to the user in 1 line.",
    backstory=(
        "Knows global travel trends and personalizes based on past user "
        "preferences: {user_preferences} in very short form."
    ),
    tools=[serper_tool],
    allow_delegation=False,
    verbose=True,
    llm=gemini_llm,
)

deal_researcher = Agent(
    role="Deal Finder",
    goal="Return only one cheapest hotel and one cheapest flight with short comments.",
    backstory="Finds best deals but only highlights the top value in minimal text.",
    tools=[serper_tool, scrape_website_tool],
    allow_delegation=False,
    verbose=True,
    llm=gemini_llm,
)

travel_planner = Agent(
    role="Travel Planner",
    goal="Give a short day-by-day bullet list (max 3 days) in 3-4 lines.",
    backstory="Converts recommendations into a sample travel sketch.",
    allow_delegation=False,
    verbose=True,
    llm=gemini_llm,
)

itinerary_generator = Agent(
    role="Itinerary Finalizer",
    goal="Give a 2-3 line itinerary summary with total cost estimate.",
    backstory="Wraps up all travel plans into an actionable summary.",
    allow_delegation=False,
    verbose=True,
    llm=gemini_llm,
)
