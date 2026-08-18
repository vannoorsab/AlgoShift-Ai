from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class CurrentReelItem(BaseModel):
    reelId: str
    title: str

class InterestDetectedItem(BaseModel):
    topic: str
    confidence: str = "High"

class RecommendedTechReelItem(BaseModel):
    candidateId: str
    title: str

class ChallengeExplanationResult(BaseModel):
    currentReel: CurrentReelItem
    interestDetected: InterestDetectedItem
    why: str
    recommendedTechReel: RecommendedTechReelItem
    category: str
    whyThisRecommendation: str
    difficulty: str
    confidence: str

class EvidenceTransparency(BaseModel):
    interestPath: List[str] = Field(default_factory=list)
    selectionFactors: List[str] = Field(default_factory=list)

class ExplainRecommendationRequest(BaseModel):
    userId: str = "student_001"
    currentReelId: str = "R003"

class ExplainRecommendationResponse(BaseModel):
    success: bool = True
    result: ChallengeExplanationResult
    evidence: EvidenceTransparency
