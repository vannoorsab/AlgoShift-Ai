from typing import List, Optional
from pydantic import BaseModel
from app.models.enums import AgentStatus

class AgentRun(BaseModel):
    id: str
    name: str
    status: AgentStatus
    summary: str
    detail: str
    durationMs: Optional[int] = None

class AgentPipeline(BaseModel):
    runId: str
    startedAt: str
    agents: List[AgentRun]
