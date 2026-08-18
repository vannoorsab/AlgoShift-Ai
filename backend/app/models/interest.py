from typing import List, Dict, Union, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.models.enums import Confidence, InterestTrend

class Interest(BaseModel):
    id: str
    name: str
    score: int = Field(ge=0, le=100)
    confidence: Confidence
    trend: InterestTrend
    relatedTopics: List[str]
    recentActivity: List[str]

class InterestInference(BaseModel):
    primaryInterest: str
    supportingSignals: List[str]
    note: str

class InterestGraphNode(BaseModel):
    id: str
    label: str
    score: int
    confidence: Confidence
    relatedTopics: List[str]
    recentActivity: List[str]

class InterestGraphEdge(BaseModel):
    from_node: str = Field(alias="from")
    to: str

    model_config = ConfigDict(populate_by_name=True)

class InterestGraph(BaseModel):
    root: str
    nodes: List[InterestGraphNode]
    edges: List[InterestGraphEdge]

class InterestTimelinePoint(BaseModel):
    date: str
    scores: Dict[str, Union[int, float, str]] = Field(default_factory=dict)

# ============================================================================
# Agent 2 Models — InterestInferenceAgent
# ============================================================================

class InterestItem(BaseModel):
    topic: str
    score: float = Field(ge=0.0, le=1.0)
    confidence: float = Field(ge=0.0, le=1.0)
    trend: str = "Stable"
    evidence: List[str] = Field(default_factory=list)

class WeakSignalItem(BaseModel):
    topic: str
    score: float = Field(ge=0.0, le=1.0)
    reason: str

class NegativeSignalItem(BaseModel):
    topic: str
    score: float = Field(ge=0.0, le=1.0)
    reason: str

class CuriosityItem(BaseModel):
    topic: str
    score: float = Field(ge=0.0, le=1.0)

class FrontierItem(BaseModel):
    topic: str
    score: float = Field(ge=0.0, le=1.0)

class InterestProfile(BaseModel):
    userId: str
    primaryInterests: List[InterestItem] = Field(default_factory=list)
    secondaryInterests: List[InterestItem] = Field(default_factory=list)
    emergingInterests: List[InterestItem] = Field(default_factory=list)
    decliningInterests: List[InterestItem] = Field(default_factory=list)
    weakSignals: List[WeakSignalItem] = Field(default_factory=list)
    negativeSignals: List[NegativeSignalItem] = Field(default_factory=list)
    curiosity: List[CuriosityItem] = Field(default_factory=list)
    interestFrontier: List[FrontierItem] = Field(default_factory=list)
    overallConfidence: float = Field(default=0.0, ge=0.0, le=1.0)
    updatedAt: Optional[str] = None
