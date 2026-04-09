from typing import List
from pydantic import BaseModel, Field


class ResearchReport(BaseModel):
    topic: str = Field(description="The core subject of the research.")
    executive_summary: str = Field(description="High-level overview.")
    academic_findings: str = Field(description="Details on methodologies and results.")
    industry_impact: str = Field(description="Real-world application details.")
    sources: List[str] = Field(description="List of all URLs and citations.")
    full_text_markdown: str = Field(description="The complete, formatted report text.")