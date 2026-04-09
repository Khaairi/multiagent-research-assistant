from typing import Dict, List

import arxiv


def search_arxiv(query: str) -> List[Dict[str, str]]:
    """
    Searches ArXiv.org for the latest academic papers and pre-prints.

    Use this tool when the user asks for scientific research, academic papers,
    or technical deep-dives into topics like AI, Physics, or Mathematics.

    Args:
        query: A specific search string or keywords (e.g., 'Large Language Models'
               or 'Quantum Computing').

    Returns:
        A list of dictionaries containing the title, summary, PDF URL,
        and publication date of the top 3 papers.
    """
    search = arxiv.Search(query=query, max_results=3)

    results = []
    for r in search.results():
        results.append(
            {
                "title": r.title,
                "summary": r.summary,
                "url": r.pdf_url,
                "published": str(r.published),
            }
        )

    print(results)
    return results