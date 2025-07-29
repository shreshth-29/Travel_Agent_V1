# app.py
from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="Agentic Travel Planner API")
app.include_router(router)
