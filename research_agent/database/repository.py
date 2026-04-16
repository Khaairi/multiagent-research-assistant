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
    # research_tasks stores follow-up tasks linked to a research report
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS research_tasks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            research_id INTEGER NOT NULL,
            task        TEXT NOT NULL,
            status      TEXT NOT NULL DEFAULT 'ongoing',
            FOREIGN KEY (research_id) REFERENCES research_results(id)
        )
        """
    )
    # web_findings stores on-demand web searches linked to a parent research row
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS web_findings (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            research_id         INTEGER,
            topic               TEXT,
            findings            TEXT,
            sources             TEXT,
            created_at          TEXT,
            FOREIGN KEY (research_id) REFERENCES research_results(id)
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
    
def save_web_findings_to_db(
    research_id: int,
    topic: str,
    findings: str,
    sources: list[str] | None = None,
) -> dict:
    """
    Saves web search findings and links them to an existing research report.
 
    Args:
        research_id: The ID of the related research report in research_results.
        topic:       The search topic or query used.
        findings:    The full web search findings text.
        sources:     Optional list of URLs found.
 
    Returns:
        A dict with ``status`` and the new row ``id`` on success.
    """
    sources = sources or []
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.execute(
            """
            INSERT INTO web_findings (research_id, topic, findings, sources, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (research_id, topic, findings, json.dumps(sources), datetime.utcnow().isoformat()),
        )
        con.commit()
        row_id = cur.lastrowid
        con.close()
        return {
            "status": "success",
            "id": row_id,
            "message": f"Web findings saved with id={row_id}, linked to research id={research_id}.",
        }
    except Exception as exc:
        return {"status": "error", "error": str(exc)}
    
def save_tasks_to_db(research_id: int, tasks: list[str]) -> dict:
    """
    Saves a list of follow-up tasks linked to a research report.
 
    Args:
        research_id: The ID of the related research report in research_results.
        tasks:       List of 3-5 task descriptions to save.
 
    Returns:
        A dict with ``status`` and the list of inserted row ``ids`` on success.
    """
    try:
        con = sqlite3.connect(DB_PATH)
        ids = []
        for task in tasks:
            cur = con.execute(
                """
                INSERT INTO research_tasks (research_id, task, status)
                VALUES (?, ?, 'ongoing')
                """,
                (research_id, task),
            )
            ids.append(cur.lastrowid)
        con.commit()
        con.close()
        return {
            "status": "success",
            "ids": ids,
            "message": f"{len(ids)} tasks saved for research id={research_id}.",
        }
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

def list_tasks_by_research(research_id: int) -> list[dict]:
    """
    Returns all tasks linked to a specific research report.
 
    Args:
        research_id: The ID of the research report.
 
    Returns:
        A list of dicts with id, task, and status.
    """
    con = sqlite3.connect(DB_PATH)
    cur = con.execute(
        """
        SELECT id, task, status
        FROM research_tasks
        WHERE research_id = ?
        ORDER BY id ASC
        """,
        (research_id,),
    )
    rows = [{"id": r[0], "task": r[1], "status": r[2]} for r in cur.fetchall()]
    con.close()
    return rows