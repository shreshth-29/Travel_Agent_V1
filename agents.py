# agents.py
from crewai import Agent
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# Load Gemini LLM with token and short output config
gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    max_output_tokens=256,  # Force short responses
    temperature=0.7
)

# Tools
serper_tool = SerperDevTool()
scrape_website_tool = ScrapeWebsiteTool()

# Agents (with very concise goals and responses)
supervisor = Agent(
    role='Travel Supervisor',
    goal='Summarize and validate the trip plan in 1-2 lines.',
    backstory='Manages the overall output but keeps it minimal and high-level.',
    allow_delegation=True,
    verbose=True,
    llm=gemini_llm
)

recommendation_agent = Agent(
    role='Recommendation Expert',
    goal='Suggest one destination or activity tailored to the user in 1 line.',
    backstory='Knows global travel trends and personalizes based on past user preferences: {user_preferences} in very short form.',
    tools=[serper_tool],
    allow_delegation=False,
    verbose=True,
    llm=gemini_llm
)

deal_researcher = Agent(
    role='Deal Finder',
    goal='Return only one cheapest hotel and one cheapest flight with short comments.',
    backstory='Finds best deals but only highlights the top value in minimal text.',
    tools=[serper_tool, scrape_website_tool],
    allow_delegation=False,
    verbose=True,
    llm=gemini_llm
)

travel_planner = Agent(
    role='Travel Planner',
    goal='Give a short day-by-day bullet list (max 3 days) in 3-4 lines.',
    backstory='Converts recommendations into a sample travel sketch.',
    allow_delegation=False,
    verbose=True,
    llm=gemini_llm
)

itinerary_generator = Agent(
    role='Itinerary Finalizer',
    goal='Give a 2-3 line itinerary summary with total cost estimate.',
    backstory='Wraps up all travel plans into an actionable summary.',
    allow_delegation=False,
    verbose=True,
    llm=gemini_llm
)















# agents.py
# Defines the various AI agents for the travel planning crew.

# from crewai import Agent
# from crewai_tools import SerperDevTool, ScrapeWebsiteTool
# import os
# # Removed load_dotenv from here, it should be in main.py as the primary entry point.

# # Initialize tools for agents. These tools allow agents to interact with external services.
# serper_tool = SerperDevTool()
# scrape_website_tool = ScrapeWebsiteTool()

# # Initialize the Google Gemini LLM here, so it can be passed to agents directly.
# # Ensure GOOGLE_API_KEY is set in your .env file
# from langchain_google_genai import ChatGoogleGenerativeAI

# gemini_llm = ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash", # You can use "gemini-pro" or other available Gemini models
#     google_api_key=os.getenv("GOOGLE_API_KEY")
# )

# # user_preferences dictionary is now defined in main.py and passed as input
# # No longer defined here

# # Define Agents
# # Each agent has a specific role, goal, backstory, and may use specific tools.
# # The 'llm' parameter is now explicitly set during agent initialization.

# # Supervisor Agent: Oversees the entire process, delegates tasks, and ensures coordination.
# supervisor = Agent(
#     role='Travel Planning Supervisor',
#     goal='Oversee the entire travel planning process, ensuring all agents work collaboratively '
#          'to deliver a comprehensive and personalized travel plan that meets the user\'s request.',
#     backstory='An experienced project manager in AI-driven travel solutions, skilled at delegating '
#               'tasks, monitoring progress, and ensuring high-quality, cohesive outputs from a team of specialized AI agents.',
#     verbose=True,
#     allow_delegation=True, # Can delegate tasks to other agents
#     llm=gemini_llm # Assign the Gemini LLM directly here
# )

# # Recommendation Agent: Provides personalized destination and activity recommendations.
# recommendation_agent = Agent(
#     role='Travel Recommendation Expert',
#     goal='Based on user preferences and historical data, recommend suitable destinations and activities '
#          'that align with their adventurous travel style, budget, and interests.',
#     # Updated backstory to expect user_preferences as a direct input from the crew's kickoff
#     backstory='A seasoned travel consultant with a deep understanding of global destinations and '
#               'adventure activities. Specializes in matching unique experiences to individual traveler profiles. '
#               'Leverages past user preferences: {user_preferences}.', # Now expects user_preferences as a direct input
#     tools=[serper_tool], # Can use search to find more ideas if needed
#     verbose=True,
#     allow_delegation=False, # Focuses on recommendations, doesn't delegate
#     llm=gemini_llm # Assign the Gemini LLM directly here
# )

# # Deal Researcher Agent: Finds the best deals for flights, accommodation, and activities.
# deal_researcher = Agent(
#     role='Travel Deal Researcher',
#     goal='Find the best flight, accommodation, and activity deals for the specified travel criteria '
#          'and budget, ensuring value for money.',
#     backstory='A meticulous financial analyst specialized in travel, constantly scanning the web '
#               'for the most cost-effective and high-value travel opportunities. '
#               'Uses advanced search and scraping tools to unearth hidden gems and discounts.',
#     tools=[serper_tool, scrape_website_tool], # Now uses Serper for search, ScrapeWebsiteTool for scraping details
#     verbose=True,
#     allow_delegation=False, # Focuses on research, doesn't delegate
#     llm=gemini_llm # Assign the Gemini LLM directly here
# )

# # Travel Planner Agent: Compiles all information into a coherent travel plan.
# travel_planner = Agent(
#     role='Comprehensive Travel Planner',
#     goal='Synthesize recommendations and deal research into a coherent, detailed travel plan '
#          'including logistics, budget breakdown, and practical advice.',
#     backstory='An expert in logistics and travel itinerary creation, known for transforming raw '
#               'data into actionable, well-structured travel blueprints. Ensures every detail, '
#               'from transport to local customs, is covered.',
#     verbose=True,
#     allow_delegation=False, # Focuses on planning, doesn't delegate
#     llm=gemini_llm # Assign the Gemini LLM directly here
# )

# # Itinerary Generator Agent: Creates a day-by-day itinerary.
# itinerary_generator = Agent(
#     role='Detailed Itinerary Creator',
#     goal='Generate a day-by-day itinerary based on the comprehensive travel plan, '
#          'including specific activities, timings, and local tips.',
#     backstory='A creative and organized itinerary specialist who crafts engaging and realistic '
#               'daily schedules, ensuring a smooth and enjoyable travel experience. '
#               'Provides practical tips for each day.',
#     verbose=True,
#     allow_delegation=False, # Focuses on itinerary generation, doesn't delegate
#     llm=gemini_llm # Assign the Gemini LLM directly here
# )
