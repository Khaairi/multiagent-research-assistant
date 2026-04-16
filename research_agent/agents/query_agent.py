from google.adk.agents.llm_agent import Agent

from research_agent.database import list_saved_research
from ._factory import make_model

query_agent = Agent(
    model=make_model(),
    name="query_agent",
    description=(
        "Answers questions about previously saved research reports. "
        "Use this for queries like 'what have I researched?', 'show my recent research', "
        "'what did I find about X?', or any question about past research history."
    ),
    instruction="""You are a Research History Assistant.

    The user wants to know about their previously saved research.

    Use `list_saved_research` to fetch recent reports from the database,
    then answer the user's question based on the results.

    Format your response clearly:
    - List each report with its ID, topic, date, and a short preview.
    - If the user asks about a specific topic, highlight the matching entries.
    - If no results are found, tell the user their database is empty.""",
    tools=[list_saved_research],
)