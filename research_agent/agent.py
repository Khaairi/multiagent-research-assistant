from research_agent.agents.pipeline import root_agent
from research_agent.database.repository import init_db

init_db()

__all__ = ["root_agent"]