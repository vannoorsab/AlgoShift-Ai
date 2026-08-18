from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, status, Body
from app.models.recommendation import (
    Recommendation, RejectedContent, CandidateGenerationResponse
)
from app.models.quality import EvaluateCandidatesResponse, EvaluateCandidatesRequest
from app.models.ranking import RankRecommendationResponse, RankRecommendationRequest
from app.models.explanation import ExplainRecommendationResponse, ExplainRecommendationRequest
from app.models.feedback import RecommendationFeedbackResponse, RecommendationFeedbackPayload
from app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

def get_recommendation_service() -> RecommendationService:
    return RecommendationService()

@router.post("/candidates", response_model=CandidateGenerationResponse, status_code=status.HTTP_200_OK)
async def generate_candidates(
    payload: Dict[str, Any] = Body(...),
    service: RecommendationService = Depends(get_recommendation_service)
) -> CandidateGenerationResponse:
    """Agent 3: CandidateGenerationAgent endpoint generating 10-20 candidates."""
    user_id = payload.get("userId", "student_001")
    user_difficulty = payload.get("difficulty", "Intermediate")
    return await service.generate_candidate_pool(user_id, user_difficulty)

@router.post("/evaluate", response_model=EvaluateCandidatesResponse, status_code=status.HTTP_200_OK)
async def evaluate_candidates(
    payload: Dict[str, Any] = Body(...),
    service: RecommendationService = Depends(get_recommendation_service)
) -> EvaluateCandidatesResponse:
    """Agent 4: ContentQualityAgent endpoint evaluating quality dimensions and decision rules."""
    user_id = payload.get("userId", "student_001")
    candidate_ids = payload.get("candidateIds")
    custom_candidates = payload.get("candidates")
    return await service.evaluate_candidate_quality(user_id, candidate_ids, custom_candidates)

@router.post("/rank", response_model=RankRecommendationResponse, status_code=status.HTTP_200_OK)
async def rank_recommendations(
    payload: Dict[str, Any] = Body(...),
    service: RecommendationService = Depends(get_recommendation_service)
) -> RankRecommendationResponse:
    """Agent 5: RecommendationRankingEngine endpoint ranking candidates and selecting top 3 recommendations."""
    user_id = payload.get("userId", "student_001")
    current_reel_id = payload.get("currentReelId", "R003")
    custom_candidates = payload.get("candidates")
    return await service.rank_recommendations(user_id, current_reel_id, custom_candidates)

@router.post("/explain", response_model=ExplainRecommendationResponse, status_code=status.HTTP_200_OK)
async def explain_recommendation(
    payload: Dict[str, Any] = Body(...),
    service: RecommendationService = Depends(get_recommendation_service)
) -> ExplainRecommendationResponse:
    """Agent 6: ExplanationAgent endpoint generating exact 8-field challenge output & evidence transparency."""
    user_id = payload.get("userId", "student_001")
    current_reel_id = payload.get("currentReelId", "R003")
    return await service.explain_recommendation(user_id, current_reel_id)

@router.post("/feedback", response_model=RecommendationFeedbackResponse, status_code=status.HTTP_200_OK)
async def process_recommendation_feedback(
    payload: RecommendationFeedbackPayload,
    service: RecommendationService = Depends(get_recommendation_service)
) -> RecommendationFeedbackResponse:
    """Agent 7: FeedbackLearningAgent endpoint processing explicit & implicit interaction feedback."""
    return await service.process_recommendation_feedback(payload)

@router.post("/generate", response_model=List[Recommendation], status_code=status.HTTP_200_OK)
async def generate_recommendations(
    payload: Dict[str, Any] = Body(...),
    service: RecommendationService = Depends(get_recommendation_service)
) -> List[Recommendation]:
    user_id = payload.get("userId", "demo-user")
    return await service.generate_recommendations(user_id)

@router.get("/user/{userId}", response_model=List[Recommendation], status_code=status.HTTP_200_OK)
async def get_user_recommendations(
    userId: str,
    service: RecommendationService = Depends(get_recommendation_service)
) -> List[Recommendation]:
    return await service.get_user_recommendations(userId)

@router.post("/{recommendationId}/feedback", status_code=status.HTTP_200_OK)
async def send_feedback(
    recommendationId: str,
    payload: Dict[str, Any] = Body(...),
    service: RecommendationService = Depends(get_recommendation_service)
):
    feedback_type = payload.get("type") or payload.get("feedback") or "LIKE"
    reason = payload.get("reason")
    await service.handle_feedback(recommendationId, feedback_type, reason)
    return {"ok": True}

@router.get("/user/{userId}/rejected", response_model=List[RejectedContent], status_code=status.HTTP_200_OK)
async def get_rejected_content(
    userId: str,
    service: RecommendationService = Depends(get_recommendation_service)
) -> List[RejectedContent]:
    return await service.get_rejected_content(userId)
