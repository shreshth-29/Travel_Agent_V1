# langgraph_version/tools.py
# Search and scrape helpers. These replace CrewAI's SerperDevTool and
# ScrapeWebsiteTool. They are plain functions called from the graph nodes
# rather than LLM-selected tools, which keeps the graph deterministic.

import os
import re

import requests

SERPER_RESULT_COUNT = 5
SCRAPE_MAX_CHARS = 2000
SCRAPE_TIMEOUT_SECONDS = 15


def search_web(query: str, num_results: int = SERPER_RESULT_COUNT) -> list[dict]:
    """Run a Serper (Google) search and return a list of {title, link, snippet}.

    Returns an empty list if SERPER_API_KEY is missing or the request fails,
    so that a search outage degrades to an LLM-only answer instead of crashing.
    """
    if not os.getenv("SERPER_API_KEY"):
        return []
    try:
        from langchain_community.utilities import GoogleSerperAPIWrapper

        wrapper = GoogleSerperAPIWrapper(k=num_results)
        raw = wrapper.results(query)
    except Exception as e:  # network, quota, missing package
        print(f"[tools] search failed for {query!r}: {e}")
        return []

    results = []
    for item in raw.get("organic", [])[:num_results]:
        results.append(
            {
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", ""),
            }
        )
    return results


def format_search_results(results: list[dict]) -> str:
    """Render search results as plain text for inclusion in a prompt."""
    if not results:
        return "(no search results available)"
    lines = []
    for r in results:
        lines.append(f"- {r['title']}\n  {r['link']}\n  {r['snippet']}")
    return "\n".join(lines)


def scrape_text(url: str, max_chars: int = SCRAPE_MAX_CHARS) -> str:
    """Fetch a page and return a rough plain-text extraction.

    Tries langchain_community's WebBaseLoader first (BeautifulSoup based). If
    that is unavailable, falls back to requests plus a tag-stripping regex.
    Returns an empty string on any failure.
    """
    try:
        from langchain_community.document_loaders import WebBaseLoader

        docs = WebBaseLoader(url).load()
        text = "\n".join(d.page_content for d in docs)
    except Exception:
        try:
            resp = requests.get(
                url,
                timeout=SCRAPE_TIMEOUT_SECONDS,
                headers={"User-Agent": "Mozilla/5.0 (travel-agent)"},
            )
            resp.raise_for_status()
            html = re.sub(r"(?is)<(script|style).*?</\1>", " ", resp.text)
            text = re.sub(r"(?s)<[^>]+>", " ", html)
        except Exception as e:
            print(f"[tools] scrape failed for {url!r}: {e}")
            return ""
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_chars]
