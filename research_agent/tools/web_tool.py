import requests

from research_agent.config import GOOGLE_API_KEY, GOOGLE_CX_ID


def search_web(query: str, num_results: int = 3) -> list[dict]:
    """
    Searches the web using Google Custom Search JSON API.

    Args:
        query:       Search query string.
        num_results: Number of results to return (max 10 per API call).

    Returns:
        List of dicts with keys: title, link, snippet.
        Returns an error dict on failure.
    """
    if not GOOGLE_API_KEY or not GOOGLE_CX_ID:
        return [{"error": "GOOGLE_API_KEY or GOOGLE_CX_ID not set in environment."}]

    try:
        response = requests.get(
            "https://www.googleapis.com/customsearch/v1",
            params={
                "key": GOOGLE_API_KEY,
                "cx": GOOGLE_CX_ID,
                "q": query,
                "num": min(num_results, 10),
            },
            timeout=10,
        )
        response.raise_for_status()
        items = response.json().get("items", [])
        return [
            {
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", ""),
            }
            for item in items
        ]
    except requests.HTTPError as exc:
        return [{"error": f"HTTP {exc.response.status_code}: {exc.response.text[:200]}"}]
    except Exception as exc:
        return [{"error": str(exc)}]