from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class RecommendationFeedbackPayload(BaseModel):
    userId: str = "student_001"
    reelId: str = "TECH014"
    eventId: Optional[str] = None
    watchPercentage: Optional[float] = Field(default=0.0, ge=0.0, le=100.0)
    liked: Optional[bool] = False
    saved: Optional[bool] = False
    shared: Optional[bool] = False
    rewatched: Optional[bool] = False
    skipped: Optional[bool] = False
    completed: Optional[bool] = False

class InterestTopicChange(BaseModel):
    topic: str
    previousScore: float
    newScore: float
    change: float

class RecommendationFeedbackResponse(BaseModel):
    success: bool = True
    updatedInterests: List[InterestTopicChange] = Field(default_factory=list)
