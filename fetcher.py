import httpx
import feedparser
from typing import List, Dict


ARXIV_API = "https://export.arxiv.org/api/query"

# Search queries covering key medical domains
SEARCH_QUERIES = [
    "cat:q-bio.NC",       # Neuroscience
    "cat:q-bio.GN",       # Genomics
    "ti:cardiology",
    "ti:dermatology",
    "ti:anesthesia",
    "ti:medicine OR ti:clinical OR ti:diagnosis",
]


def fetch_papers(query: str, max_results: int = 10) -> List[Dict]:
    """Fetch paper abstracts from arXiv for a given query."""
    params = {
        "search_query": query,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }

    with httpx.Client(timeout=30) as client:
        response = client.get(ARXIV_API, params=params)
        response.raise_for_status()

    feed = feedparser.parse(response.text)
    papers = []

    for entry in feed.entries:
        papers.append({
            "id": entry.get("id", ""),
            "title": entry.get("title", "").strip().replace("\n", " "),
            "summary": entry.get("summary", "").strip().replace("\n", " "),
            "authors": [a.name for a in entry.get("authors", [])],
            "published": entry.get("published", ""),
            "link": entry.get("link", ""),
        })

    return papers


def fetch_all_papers(max_per_query: int = 5) -> List[Dict]:
    """Fetch papers from all queries, deduplicated by arXiv ID."""
    seen_ids = set()
    all_papers = []

    for query in SEARCH_QUERIES:
        try:
            papers = fetch_papers(query, max_results=max_per_query)
            for paper in papers:
                if paper["id"] not in seen_ids:
                    seen_ids.add(paper["id"])
                    all_papers.append(paper)
        except Exception as e:
            print(f"[Fetcher] Failed to fetch query={query}: {e}")

    print(f"[Fetcher] Total papers fetched: {len(all_papers)}")
    return all_papers
