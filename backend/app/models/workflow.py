from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from app.models.explanation import ChallengeExplanationResult, EvidenceTransparency

class WorkflowStepStatus(BaseModel):
    agent: str
    status: str = "completed"
    durationMs: int = 0
    error: Optional[str] = None

class WorkflowError(BaseModel):
    step: str
    code: str
    message: str

class AnalyzeRequest(BaseModel):
    userId: str = "student_001"
    inputMode: str = "dataset"
    url: Optional[str] = None
    reelId: Optional[str] = None

class AnalyzeNextRequest(BaseModel):
    userId: str = "student_001"

class AnalyzeResponse(BaseModel):
    success: bool
    runId: str
    result: Optional[ChallengeExplanationResult] = None
    evidence: Optional[EvidenceTransparency] = None
    workflow: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[WorkflowError] = None

class WorkflowRunDoc(BaseModel):
    runId: str
    userId: str
    inputMode: str
    status: str = "completed"
    steps: List[WorkflowStepStatus] = Field(default_factory=list)
    result: Optional[Dict[str, Any]] = None
    startedAt: str
    completedAt: Optional[str] = None
    failedStep: Optional[str] = None
