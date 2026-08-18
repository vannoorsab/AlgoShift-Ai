from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from app.models.enums import Category, Difficulty, HistoryEventKind, AgentStatus

class HistoryEvent(BaseModel):
    id: str
    kind: HistoryEventKind
    title: str
    description: str
    timestamp: str

class KpiSummary(BaseModel):
    recommendationsGenerated: int
    recommendationsAccepted: int
    usefulContentPct: int
    hypeContentRejected: int
    topInterest: str

class RecommendationAcceptancePoint(BaseModel):
    label: str
    accepted: int
    rejected: int

class CategoryDistributionPoint(BaseModel):
    category: str
    value: int

class EducationalValuePoint(BaseModel):
    label: str
    value: int

class HypeRejectionPoint(BaseModel):
    label: str
    rejected: int
    approved: int

class DifficultyDistributionPoint(BaseModel):
    difficulty: str
    value: int

class Analytics(BaseModel):
    kpis: KpiSummary
    interestEvolution: List[Dict[str, Any]]
    recommendationAcceptance: List[RecommendationAcceptancePoint]
    categoryDistribution: List[CategoryDistributionPoint]
    educationalValue: List[EducationalValuePoint]
    hypeRejectionRate: List[HypeRejectionPoint]
    difficultyDistribution: List[DifficultyDistributionPoint]

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

class RecommendationControls(BaseModel):
    moreEducational: int
    moreCareerFocused: int
    moreTechnical: int
    moreDiverse: int

class UserSettings(BaseModel):
    preferredDifficulty: Difficulty
    contentPreferences: List[Category]
    recommendationControls: RecommendationControls
    hypeSensitivity: int

class User(BaseModel):
    id: str
    name: str
    email: Optional[str] = None
    settings: UserSettings
