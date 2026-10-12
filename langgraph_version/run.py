# langgraph_version/run.py
# LangGraph backend entry point. Exposes run_agentic_flow(trip_details) with
# the same signature and return shape as crewai_version/main.py so the FastAPI
# and Streamlit front ends can switch between backends with AGENT_BACKEND.

from settings import load_env

load_env()

from langgraph_version.graph import build_graph  # noqa: E402

FALLBACK_MESSAGE = (
    "Travel plan could not be generated due to an internal error "
    "(often a Gemini API rate limit). Quick fallback suggestion: visit "
    "Thailand for 7 days and explore Bangkok and Krabi."
)

_graph = None


def get_graph():
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph


def format_result(state: dict) -> str:
    """Join the node outputs into one markdown document.

    The CrewAI backend returns only the last task's output (the supervisor's
    validation line). Here the full plan is returned, with the validation
    status at the end, since that is what the front ends display.
    """
    sections = [
        ("Deals", state.get("deals", "")),
        ("Recommendation", state.get("recommendations", "")),
        ("Itinerary", state.get("itinerary", "")),
        ("Summary", state.get("report", "")),
        ("Status", state.get("validation", "")),
    ]
    return "\n\n".join(f"## {title}\n{body.strip()}" for title, body in sections if body)


def run_agentic_flow(trip_details: dict) -> dict:
    """Run the graph on one trip request and return {"result": markdown_string}."""
    print("## Initiating Travel Planning Process (LangGraph)...\n")
    try:
        final_state = get_graph().invoke({"trip_details": trip_details})
        print("\n## Travel Planning Complete!")
        return {"result": format_result(final_state)}
    except Exception as e:
        print(f"Agentic flow failed: {e}")
        return {"result": FALLBACK_MESSAGE}


if __name__ == "__main__":
    from examples.demo_request import DEMO_TRIP_DETAILS

    result = run_agentic_flow(DEMO_TRIP_DETAILS)
    print("Here's your travel plan:\n")
    print(result["result"])
