from typing import List, Optional, Union, Dict, Any
from pydantic import BaseModel, Field
from app.models.enums import SourceType, Difficulty, Confidence

class Reel(BaseModel):
    id: str
    title: str
    thumbnailUrl: Optional[str] = None
    topic: str
    broaderInterest: str
    context: str

class NormalizedReelContent(BaseModel):
    reelId: str
    sourceType: SourceType = SourceType.DEMO
    sourceUrl: Optional[str] = None
    title: Optional[str] = ""
    caption: Optional[str] = ""
    hashtags: List[str] = Field(default_factory=list)
    transcript: Optional[str] = ""
    ocrText: Optional[str] = ""
    visualDescription: Optional[str] = ""
    mediaMetadata: Dict[str, Any] = Field(default_factory=dict)

# Alias for backward compatibility
ReelContent = NormalizedReelContent

class ReelAnalysis(BaseModel):
    reelId: str
    primaryTopic: str
    broaderDomain: str
    subtopics: List[str] = Field(default_factory=list)
    context: str
    intent: str
    concepts: List[str] = Field(default_factory=list)
    educationalValue: float = Field(ge=0.0, le=1.0)
    careerRelevance: float = Field(ge=0.0, le=1.0)
    technicalDepth: float = Field(ge=0.0, le=1.0)
    entertainmentValue: float = Field(ge=0.0, le=1.0)
    hypeScore: float = Field(ge=0.0, le=1.0)
    clickbaitScore: float = Field(ge=0.0, le=1.0)
    difficulty: Difficulty
    confidence: float = Field(ge=0.0, le=1.0)

class ReelAnalysisInput(BaseModel):
    reelId: Optional[str] = "R001"
    sourceType: SourceType = SourceType.DEMO
    sourceUrl: Optional[str] = None
    title: Optional[str] = ""
    caption: Optional[str] = ""
    hashtags: List[str] = Field(default_factory=list)
    transcript: Optional[str] = ""
    ocrText: Optional[str] = ""
    visualDescription: Optional[str] = ""
    mediaMetadata: Dict[str, Any] = Field(default_factory=dict)
    url: Optional[str] = None

class AnalyzeReelRequest(BaseModel):
    reelId: Optional[str] = "R001"
    sourceType: SourceType = SourceType.DEMO
    sourceUrl: Optional[str] = None
    title: Optional[str] = ""
    caption: Optional[str] = ""
    hashtags: List[str] = Field(default_factory=list)
    transcript: Optional[str] = ""
    ocrText: Optional[str] = ""
    visualDescription: Optional[str] = ""
    mediaMetadata: Dict[str, Any] = Field(default_factory=dict)

class AnalyzeReelResponse(BaseModel):
    success: bool = True
    analysis: ReelAnalysis

class StoredReelRecord(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    reelId: str
    sourceType: str
    sourceUrl: Optional[str] = None
    content: dict
    analysis: dict
    analysisVersion: str = "1.0"
    createdAt: str
    updatedAt: str
