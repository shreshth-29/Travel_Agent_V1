# settings.py
# Small shared helpers used by both backends and both front ends.

import os

from dotenv import load_dotenv

BACKENDS = ("crewai", "langgraph")


def load_env() -> None:
    """Load API keys from .env (preferred) or the legacy travelagent.env.

    Variables already present in the process environment are not overridden,
    so values set by Docker, Render or the shell take precedence.
    """
    load_dotenv(".env")
    load_dotenv("travelagent.env")


def get_backend(override: str | None = None) -> str:
    """Return the backend name: the override if given, else AGENT_BACKEND, else crewai."""
    name = (override or os.getenv("AGENT_BACKEND") or "crewai").strip().lower()
    if name not in BACKENDS:
        raise ValueError(f"Unknown AGENT_BACKEND {name!r}; expected one of {BACKENDS}")
    return name


def get_runner(override: str | None = None):
    """Return the run_agentic_flow function for the selected backend.

    Imports are done lazily so that only the selected backend's dependencies
    need to be installed.
    """
    name = get_backend(override)
    if name == "langgraph":
        from langgraph_version.run import run_agentic_flow
    else:
        from crewai_version.main import run_agentic_flow
    return run_agentic_flow
