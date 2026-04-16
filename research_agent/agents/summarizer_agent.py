from google.adk.agents.llm_agent import Agent

from research_agent.models import ResearchReport
from ._factory import make_model

summarizer_agent = Agent(
    model=make_model(),
    name="summarizer_agent",
    description="Synthesizes academic and web findings into a final executive report.",
    instruction="""You are a Research Lead.
    You will receive a collection of academic papers.

    **Paper result:**
    {paper_agent_output}

    Your task is to synthesize this into a structured report with:
    - Executive Summary (High-level overview)
    - Key Academic Findings (Methodologies/Results)
    - Bibliography/Links
    Maintain a professional, academic tone and do not omit source links.""",
    output_schema=ResearchReport,
)