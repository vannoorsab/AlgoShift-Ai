from typing import Optional
from pydantic import BaseModel, Field
from app.models.enums import FeedbackType, InteractionType

class Interaction(BaseModel):
    userId: str = "student_001"
    reelId: str
    type: Optional[InteractionType] = None
    watchPercentage: float = Field(default=100.0, ge=0.0, le=100.0)
    liked: bool = False
    saved: bool = False
    shared: bool = False
    rewatched: bool = False
    action: str = "viewed"
    timestamp: str

class FeedbackPayload(BaseModel):
    recommendationId: str
    feedback: FeedbackType
