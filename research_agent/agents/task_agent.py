from google.adk.agents.llm_agent import Agent
 
from research_agent.database import save_tasks_to_db
from ._factory import make_model

task_agent = Agent(
    model=make_model(),
    name="task_agent",
    description="Generates follow-up research tasks and saves them to the database.",
    instruction="""You are a Research Planning Specialist.
 
    A research report has just been saved to the database. You will find the
    assigned research ID inside `database_agent_output`.
 
    Your job:
    1. Read the summarized research from the session context.
    2. Generate 3 to 5 concrete, actionable follow-up tasks a researcher should
       do next. Tasks should be specific — not generic advice.
       Examples:
       - "Replicate the experiment in [paper X] using dataset Y"
       - "Compare methodology A vs B on benchmark Z"
       - "Search for industry adoption of [technique] in the healthcare sector"
 
    3. Extract the research_id from `database_agent_output` (look for the "id" field).
 
    4. Call `save_tasks_to_db` with:
       - research_id: the integer ID extracted above
       - tasks: the list of task strings you generated
 
    5. Present the saved tasks to the user as a numbered list and confirm they
       have been saved with their task IDs.""",
    tools=[save_tasks_to_db],
    output_key="task_agent_output",
)