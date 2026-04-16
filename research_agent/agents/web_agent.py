from google.adk.agents.llm_agent import Agent

from research_agent.tools import search_web
from research_agent.database import save_web_findings_to_db
from ._factory import make_model

web_agent = Agent(
    model=make_model(),
    name="web_agent",
    description=(
        "Searches the web for recent industry news, white papers, and applications. "
        "Use when the user asks: 'what about news for this research', "
        "'search news about X', 'find industry applications of X', "
        "'what are companies doing with X'."
    ),
    instruction="""You are an Industry Research Specialist.
 
    1. Use `search_web` to find recent news, white papers, and industry applications
       relevant to the user's query.
 
    2. Present the findings clearly:
       - Title
       - URL
       - Short summary of relevance
 
    3. After presenting, ALWAYS ask the user:
       "Would you like to save these findings to the database?
        If yes, please provide the research ID they belong to
        (you can check with 'list my research' if unsure)."
 
    4. If the user confirms with a research ID, call `save_web_findings_to_db` with:
       - research_id: the ID the user provided
       - topic: the search query you used
       - findings: the full formatted text you found
       - sources: list of all URLs you found
 
    5. Confirm the save with the assigned database ID.""",
    tools=[search_web, save_web_findings_to_db],
    output_key="web_agent_output",
)