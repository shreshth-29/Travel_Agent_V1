# api/routes.py
from fastapi import APIRouter
from api.schemas import TripRequest
from main import run_agentic_flow

router = APIRouter()

@router.post("/plan-trip")
def plan_trip(request: TripRequest):
    result = run_agentic_flow(request.trip_details)
    return result
