from google.adk.agents import ParallelAgent, SequentialAgent

from .paper_agent import paper_agent
from .web_agent import web_agent
from .summarizer_agent import summarizer_agent
from .database_agent import database_agent

parallel_research_agent = ParallelAgent(
    name="parallel_research_agent",
    description="Runs paper and web research agents in parallel.",
    sub_agents=[paper_agent, web_agent],
)

root_agent = SequentialAgent(
    name="research_manager",
    description=(
        "Full research pipeline: parallel web + paper search → "
        "summarization → database storage."
    ),
    sub_agents=[
        parallel_research_agent,  # 1. gather: web + arxiv in parallel
        summarizer_agent,          # 2. synthesize into a structured report
        database_agent,            # 3. persist report to DB
    ],
)