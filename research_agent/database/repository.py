import json
import sqlite3
from datetime import datetime

from research_agent.config import DB_PATH


def init_db() -> None:
    """Creates the research_results table if it doesn't exist."""
    con = sqlite3.connect(DB_PATH)
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS research_results (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            topic       TEXT,
            report      TEXT,
            sources     TEXT,
            created_at  TEXT
        )
        """
    )
    con.commit()
    con.close()


def save_research_to_db(
    topic: str,
    report: str,
    sources: list[str] | None = None,
) -> dict:
    """
    Saves a finished research report to the SQLite database.

    Args:
        topic:   The research topic / query that was investigated.
        report:  The full synthesized report text produced by the summarizer agent.
        sources: Optional list of source URLs or citation strings extracted from
                 the report. Pass an empty list if none are available.

    Returns:
        A dict with ``status`` ("success" or "error") and the new row ``id``
        on success, or an ``error`` message on failure.
    """
    sources = sources or []
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.execute(
            """
            INSERT INTO research_results (topic, report, sources, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (topic, report, json.dumps(sources), datetime.utcnow().isoformat()),
        )
        con.commit()
        row_id = cur.lastrowid
        con.close()
        return {"status": "success", "id": row_id, "message": f"Report saved with id={row_id}."}
    except Exception as exc:
        return {"status": "error", "error": str(exc)}


def list_saved_research(limit: int = 10) -> list[dict]:
    """
    Returns the most recent research reports stored in the database.

    Args:
        limit: Maximum number of rows to return (default 10).

    Returns:
        A list of dicts, each containing id, topic, created_at, and a
        truncated preview of the report.
    """
    con = sqlite3.connect(DB_PATH)
    cur = con.execute(
        """
        SELECT id, topic, created_at, substr(report, 1, 200) AS preview
        FROM research_results
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    )
    rows = [
        {"id": r[0], "topic": r[1], "created_at": r[2], "preview": r[3]}
        for r in cur.fetchall()
    ]
    con.close()
    return rows