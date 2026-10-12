# api/routes.py
from fastapi import APIRouter

from api.schemas import TripRequest
from settings import get_backend, get_runner

router = APIRouter()


@router.post("/plan-trip")
def plan_trip(request: TripRequest):
    """Run the selected backend on the request and return {"result": markdown}.

    The backend is chosen per request from request.backend if given, otherwise
    from the AGENT_BACKEND environment variable (default crewai).
    """
    run_agentic_flow = get_runner(request.backend)
    result = run_agentic_flow(request.trip_details)
    result["backend"] = get_backend(request.backend)
    return result
