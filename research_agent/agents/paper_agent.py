from google.adk.agents.llm_agent import Agent

from research_agent.tools import search_arxiv
from ._factory import make_model

paper_agent = Agent(
    model=make_model(),
    name="paper_agent",
    description="Specialist in searching and summarizing arXiv academic papers.",
    instruction="Search for peer-reviewed papers and summarize methodologies and results.",
    tools=[search_arxiv],
    output_key="paper_agent_output",
)