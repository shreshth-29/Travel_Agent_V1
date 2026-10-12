# api/schemas.py
from typing import Dict, Optional

from pydantic import BaseModel


class TripRequest(BaseModel):
    trip_details: Dict
    backend: Optional[str] = None  # "crewai" or "langgraph"; defaults to AGENT_BACKEND
