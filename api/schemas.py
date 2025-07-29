# api/schemas.py
from pydantic import BaseModel
from typing import Dict

class TripRequest(BaseModel):
    trip_details: Dict
