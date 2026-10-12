# app.py
# FastAPI entry point. Run with: uvicorn app:app --reload
# Select the backend with AGENT_BACKEND=crewai (default) or AGENT_BACKEND=langgraph.

from fastapi import FastAPI

from api.routes import router
from settings import get_backend, load_env

load_env()

app = FastAPI(title="Agentic Travel Planner API")
app.include_router(router)


@app.get("/")
def root():
    return {"status": "ok", "backend": get_backend()}
