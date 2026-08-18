from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field
from app.models.enums import Category, Confidence, Difficulty

class CandidateType(str, Enum):
    FAMILIAR = "Familiar"
    ADJACENT = "Adjacent"
    EXPLORATORY = "Exploratory"

class RecommendationScoreBreakdown(BaseModel):
    interestMatch: int
    educationalValue: int
    novelty: int
    careerRelevance: int
    difficultyFit: int
    diversity: int
    hypePenalty: int

class Recommendation(BaseModel):
    id: str
    title: str
    category: Category
    difficulty: Difficulty
    confidence: Confidence
    relevance: int = Field(ge=0, le=100)
    educationalValue: int = Field(ge=0, le=100)
    why: str
    recentSignals: List[str]
    underlyingInterest: str
    recommendationPath: List[str]
    scoreBreakdown: RecommendationScoreBreakdown

class RejectedContent(BaseModel):
    id: str
    title: str
    hypeScore: int
    educationalValue: int
    evidenceQuality: int
    status: str = "REJECTED"
    reason: str

# ============================================================================
# Agent 3 Models — CandidateGenerationAgent
# ============================================================================

class CandidateItem(BaseModel):
    candidateId: str
    title: str
    topic: str
    category: str
    candidateType: CandidateType
    description: str
    source: str = "demo"
    interestPath: List[str] = Field(default_factory=list)
    interestMatch: float = Field(ge=0.0, le=1.0)
    novelty: float = Field(ge=0.0, le=1.0)
    learningPotential: float = Field(ge=0.0, le=1.0)
    difficulty: Difficulty
    generationConfidence: float = Field(ge=0.0, le=1.0)

class CandidateGenerationResponse(BaseModel):
    success: bool = True
    candidateCount: int
    candidates: List[CandidateItem]
