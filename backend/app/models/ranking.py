from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class RankingScoreBreakdown(BaseModel):
    interestMatch: float = Field(ge=0.0, le=1.0)
    educationalValue: float = Field(ge=0.0, le=1.0)
    practicalUsefulness: float = Field(ge=0.0, le=1.0)
    novelty: float = Field(ge=0.0, le=1.0)
    interestExpansion: float = Field(ge=0.0, le=1.0)
    difficultyFit: float = Field(ge=0.0, le=1.0)
    careerRelevance: float = Field(ge=0.0, le=1.0)
    diversity: float = Field(ge=0.0, le=1.0)
    qualityScore: float = Field(ge=0.0, le=1.0)
    hypePenalty: float = Field(default=0.0)
    clickbaitPenalty: float = Field(default=0.0)
    duplicatePenalty: float = Field(default=0.0)
    rejectionPenalty: float = Field(default=0.0)
    finalScore: float = Field(ge=0.0, le=1.0)

class RankedCandidateItem(BaseModel):
    candidateId: str
    rank: int
    finalScore: float
    title: str
    topic: str = "APIs"
    category: str = "Backend"
    candidateType: str = "Adjacent"
    difficulty: str = "Intermediate"
    scoreBreakdown: RankingScoreBreakdown
    selectionFactors: List[str] = Field(default_factory=list)

class SelectedRecommendation(BaseModel):
    candidateId: str
    rank: int
    finalScore: float
    candidateType: str

class RankRecommendationRequest(BaseModel):
    userId: str = "student_001"
    currentReelId: str = "R003"

class RankRecommendationResponse(BaseModel):
    userId: str
    currentReelId: str
    selectedRecommendation: SelectedRecommendation
    topCandidates: List[RankedCandidateItem]
