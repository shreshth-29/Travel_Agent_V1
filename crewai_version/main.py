# crewai_version/main.py
# CrewAI backend. Builds a hierarchical crew (the supervisor's LLM acts as the
# manager) and exposes run_agentic_flow(trip_details) -> {"result": str}.

from settings import load_env

load_env()  # must run before agents.py constructs tools and the LLM

from crewai import Crew, Process  # noqa: E402

from crewai_version.agents import (  # noqa: E402
    deal_researcher,
    itinerary_generator,
    recommendation_agent,
    supervisor,
    travel_planner,
)
from crewai_version.tasks import (  # noqa: E402
    generate_recommendations_task,
    generate_report_task,
    plan_itinerary_task,
    research_deals_task,
    validate_plan_task,
)

FALLBACK_MESSAGE = (
    "Travel plan could not be generated due to an internal error "
    "(often a Gemini API rate limit). Quick fallback suggestion: visit "
    "Thailand for 7 days and explore Bangkok and Krabi."
)


def build_crew() -> Crew:
    return Crew(
        agents=[
            supervisor,
            recommendation_agent,
            deal_researcher,
            travel_planner,
            itinerary_generator,
        ],
        tasks=[
            research_deals_task,
            generate_recommendations_task,
            plan_itinerary_task,
            generate_report_task,
            validate_plan_task,
        ],
        process=Process.hierarchical,
        manager_llm=supervisor.llm,
        verbose=True,
    )


def run_agentic_flow(trip_details: dict) -> dict:
    """Run the crew on one trip request.

    trip_details keys used by the tasks: origin, destination, start_date,
    end_date, num_travelers, interests, travel_style, user_preferences.
    Extra keys (budget_preference, natural_language_request) are passed
    through and available to the manager.
    """
    project_crew = build_crew()
    print("## Initiating Travel Planning Process...\n")
    try:
        result = project_crew.kickoff(inputs=trip_details)
        print("\n## Travel Planning Complete!")
        return {"result": str(result)}
    except Exception as e:  # keep the API responsive on quota errors
        print(f"Agentic flow failed: {e}")
        return {"result": FALLBACK_MESSAGE}


if __name__ == "__main__":
    from examples.demo_request import DEMO_TRIP_DETAILS

    result = run_agentic_flow(DEMO_TRIP_DETAILS)
    print("Here's your travel plan:\n")
    print(result["result"])
