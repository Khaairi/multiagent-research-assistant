from google.adk.agents.llm_agent import Agent
from google.adk.agents import ParallelAgent, SequentialAgent

from .paper_agent import paper_agent
from .web_agent import web_agent
from .summarizer_agent import summarizer_agent
from .database_agent import database_agent
from .query_agent import query_agent
from .task_agent import task_agent
from ._factory import make_model

# parallel_research_agent = ParallelAgent(
#     name="parallel_research_agent",
#     description="Runs paper and web research agents in parallel.",
#     sub_agents=[paper_agent],
# )
 
research_pipeline_agent = SequentialAgent(
    name="research_pipeline_agent",
    description=(
        "Full academic research pipeline: searches arXiv for papers, "
        "synthesizes a report, saves it to the database, and generates follow-up tasks. "
        "Use for: 'research X', 'find papers on X', 'academic research about X'."
    ),
    sub_agents=[
        paper_agent,  # 1. gather paper from arxiv
        summarizer_agent,          # 2. synthesize into a structured report
        database_agent,            # 3. persist report to DB
        task_agent,        # 4. generate & save follow-up tasks linked to research id
    ],
)

root_agent = Agent(
    model=make_model(),
    name="research_manager",
    description="Routes user requests to the right agent.",
    instruction="""You are a Research Manager. Your job is to route the user's request to the right agent.
 
    Sub-agents:
    - `research_pipeline_agent`: Use this when the user wants to research a NEW topic.
      Triggers: "research X", "find papers about X", "look up X", "investigate X".

    - `web_agent`: User wants industry news, recent applications, or web search results.
      Can be for a new topic OR as a follow-up to an existing research report.
      Triggers: "news about X", "what about news for this research",
      "search news about X", "industry applications of X", "what are companies doing with X".

    - `query_agent`: Use this when the user asks about PAST or SAVED research.
      Triggers: "what have I researched?", "show my history", "what did I find about X?",
      "list my research", "recent research", "what's in my database?".
 
    Rules:
    1. Carefully read the user's message to determine their intent.
    2. Delegate to the correct sub-agent — do NOT answer directly yourself.
    3. If intent is ambiguous, ask the user one clarifying question.""",
    sub_agents=[research_pipeline_agent, web_agent, query_agent],
)