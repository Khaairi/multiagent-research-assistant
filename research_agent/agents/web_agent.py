from google.adk.agents.llm_agent import Agent

from research_agent.tools import search_web
from ._factory import make_model

web_agent = Agent(
    model=make_model(),
    name="web_agent",
    description="Specialist in searching the general web for industry trends and news.",
    instruction="""
        Use the search_web tool to find recent industry applications, white papers, and news.
        For every relevant result you find, you MUST provide:
        1. The Title of the article/page.
        2. The URL Link.
        3. A concise summary of why it is relevant.
        Ensure the output is clean and formatted as a list.
    """,
    tools=[search_web],
    output_key="web_agent_output",
)