# run.py
# Command line entry point. Examples:
#   python run.py                      # CrewAI backend (or AGENT_BACKEND), demo request
#   python run.py --backend langgraph  # LangGraph backend, demo request
#   python run.py --backend langgraph --request my_trip.json

import argparse
import json

from settings import BACKENDS, get_backend, get_runner, load_env


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the travel planning agent.")
    parser.add_argument(
        "--backend",
        choices=BACKENDS,
        default=None,
        help="Which backend to use. Defaults to AGENT_BACKEND or crewai.",
    )
    parser.add_argument(
        "--request",
        default=None,
        help="Path to a JSON file with trip_details. Defaults to the built-in demo request.",
    )
    args = parser.parse_args()

    load_env()
    if args.request:
        with open(args.request, encoding="utf-8") as f:
            trip_details = json.load(f)
    else:
        from examples.demo_request import DEMO_TRIP_DETAILS

        trip_details = DEMO_TRIP_DETAILS

    backend = get_backend(args.backend)
    print(f"Backend: {backend}")
    result = get_runner(backend)(trip_details)
    print("\nHere's your travel plan:\n")
    print(result["result"])


if __name__ == "__main__":
    main()
