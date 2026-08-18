from typing import List, Optional
from pydantic import BaseModel
from app.models.enums import Category, Difficulty

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
