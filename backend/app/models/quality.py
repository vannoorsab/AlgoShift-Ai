from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field

class QualityDecision(str, Enum):
    ACCEPT = "ACCEPT"
    PENALIZE = "PENALIZE"
    REJECT = "REJECT"

class QualityAssessment(BaseModel):
    candidateId: str
    educationalValue: float = Field(ge=0.0, le=1.0)
    practicalUsefulness: float = Field(ge=0.0, le=1.0)
    technicalDepth: float = Field(ge=0.0, le=1.0)
    careerRelevance: float = Field(ge=0.0, le=1.0)
    evidenceQuality: float = Field(ge=0.0, le=1.0)
    entertainmentValue: float = Field(ge=0.0, le=1.0)
    hypeScore: float = Field(ge=0.0, le=1.0)
    clickbaitScore: float = Field(ge=0.0, le=1.0)
    promotionalScore: float = Field(ge=0.0, le=1.0)
    misleadingClaimRisk: float = Field(ge=0.0, le=1.0)
    qualityScore: float = Field(ge=0.0, le=1.0)
    decision: QualityDecision
    reasons: List[str] = Field(default_factory=list)

class EvaluateCandidatesRequest(BaseModel):
    userId: str = "student_001"
    candidateIds: Optional[List[str]] = None
    candidates: Optional[List[Dict[str, Any]]] = None

class EvaluateCandidatesResponse(BaseModel):
    success: bool = True
    evaluatedCount: int
    acceptedCount: int
    penalizedCount: int
    rejectedCount: int
    evaluations: List[QualityAssessment]
