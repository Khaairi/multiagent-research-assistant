from google.adk.agents.llm_agent import Agent

from research_agent.database import save_research_to_db, list_saved_research
from ._factory import make_model

database_agent = Agent(
    model=make_model(),
    name="database_agent",
    description="Persists the finished research report to a SQLite database.",
    instruction="""You are a Data Persistence Specialist.

    You will receive a JSON object with:
    - topic: The core subject of the research.
    - executive_summary: High-level overview.
    - academic_findings: Details on methodologies and results.
    - industry_impact: Real-world application details.
    - sources: List of all URLs and citations.
    - full_text_markdown: The complete, formatted report text.

    1. Use the 'topic' field directly.
    2. Use the 'sources' list directly.
    3. Use the 'full_text_markdown' as the report content.

    Call `save_research_to_db` with these fields and confirm the assigned database ID.
    Do NOT alter or summarize the report — store it exactly as received.""",
    tools=[save_research_to_db, list_saved_research],
    output_key="database_agent_output",
)