# langgraph_version/graph.py
# A LangGraph StateGraph that mirrors the five CrewAI tasks as five nodes
# executed in a fixed order:
#
#   research_deals -> generate_recommendations -> plan_itinerary
#     -> generate_report -> validate_plan
#
# Each node reads what it needs from the shared state, calls Gemini once, and
# writes a single field back. The two research nodes also call the Serper
# search helper (and the deals node scrapes the top hit) before prompting.

import os
from typing import TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph

from langgraph_version import prompts
from langgraph_version.tools import format_search_results, scrape_text, search_web


class TripDetails(TypedDict, total=False):
    origin: str
    destination: str
    start_date: str
    end_date: str
    num_travelers: str
    budget_preference: str
    interests: str
    travel_style: str
    natural_language_request: str
    user_preferences: str


class GraphState(TypedDict, total=False):
    trip_details: TripDetails
    deals: str
    recommendations: str
    itinerary: str
    report: str
    validation: str


# One shared model, configured the same way as crewai_version/agents.py.
def make_llm() -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        max_output_tokens=int(os.getenv("MAX_OUTPUT_TOKENS", "256")),
        temperature=0.7,
    )


_llm = None


def get_llm() -> ChatGoogleGenerativeAI:
    global _llm
    if _llm is None:
        _llm = make_llm()
    return _llm


def _fields(state: GraphState) -> dict:
    """Flatten trip_details and the result fields into one dict for str.format."""
    fields = {
        "origin": "",
        "destination": "",
        "start_date": "",
        "end_date": "",
        "num_travelers": "",
        "budget_preference": "",
        "interests": "",
        "travel_style": "",
        "natural_language_request": "",
        "user_preferences": "",
        "deals": "",
        "recommendations": "",
        "itinerary": "",
        "report": "",
        "validation": "",
        "search_results": "",
    }
    fields.update(state.get("trip_details", {}))
    for key in ("deals", "recommendations", "itinerary", "report", "validation"):
        if state.get(key):
            fields[key] = state[key]
    return fields


def _ask(node_name: str, template: str, fields: dict) -> str:
    """Send one system + human message pair to Gemini and return the text."""
    system = prompts.SYSTEM_PROMPTS[node_name].format(**fields)
    human = template.format(**fields)
    response = get_llm().invoke([SystemMessage(content=system), HumanMessage(content=human)])
    return response.content if isinstance(response.content, str) else str(response.content)


# ---------------------------------------------------------------- nodes ----

def research_deals(state: GraphState) -> dict:
    fields = _fields(state)
    results = search_web(prompts.DEALS_SEARCH_QUERY.format(**fields))
    text = format_search_results(results)
    if results and os.getenv("SCRAPE_TOP_RESULT", "1") == "1":
        page = scrape_text(results[0]["link"])
        if page:
            text += f"\n\nExcerpt from {results[0]['link']}:\n{page}"
    fields["search_results"] = text
    return {"deals": _ask("research_deals", prompts.RESEARCH_DEALS, fields)}


def generate_recommendations(state: GraphState) -> dict:
    fields = _fields(state)
    results = search_web(prompts.RECOMMENDATIONS_SEARCH_QUERY.format(**fields))
    fields["search_results"] = format_search_results(results)
    return {
        "recommendations": _ask(
            "generate_recommendations", prompts.GENERATE_RECOMMENDATIONS, fields
        )
    }


def plan_itinerary(state: GraphState) -> dict:
    fields = _fields(state)
    return {"itinerary": _ask("plan_itinerary", prompts.PLAN_ITINERARY, fields)}


def generate_report(state: GraphState) -> dict:
    fields = _fields(state)
    return {"report": _ask("generate_report", prompts.GENERATE_REPORT, fields)}


def validate_plan(state: GraphState) -> dict:
    fields = _fields(state)
    return {"validation": _ask("validate_plan", prompts.VALIDATE_PLAN, fields)}


# ---------------------------------------------------------------- graph ----

NODE_ORDER = [
    ("research_deals", research_deals),
    ("generate_recommendations", generate_recommendations),
    ("plan_itinerary", plan_itinerary),
    ("generate_report", generate_report),
    ("validate_plan", validate_plan),
]


def build_graph():
    """Compile the linear five-node graph."""
    builder = StateGraph(GraphState)
    for name, fn in NODE_ORDER:
        builder.add_node(name, fn)
    builder.add_edge(START, NODE_ORDER[0][0])
    for (prev, _), (nxt, _) in zip(NODE_ORDER, NODE_ORDER[1:]):
        builder.add_edge(prev, nxt)
    builder.add_edge(NODE_ORDER[-1][0], END)
    return builder.compile()
