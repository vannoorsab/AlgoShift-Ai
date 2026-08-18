from typing import List
from fastapi import APIRouter, Depends, status
from app.models.history import HistoryEvent, Analytics, AgentPipeline
from app.models.user import UserSettings
from app.models.recommendation import Recommendation, RejectedContent
from app.services.history_service import HistoryService, AnalyticsService, AgentService, UserService
from app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/users", tags=["Users"])

def get_history_service() -> HistoryService:
    return HistoryService()

def get_analytics_service() -> AnalyticsService:
    return AnalyticsService()

def get_agent_service() -> AgentService:
    return AgentService()

def get_user_service() -> UserService:
    return UserService()

def get_recommendation_service() -> RecommendationService:
    return RecommendationService()

@router.get("/{userId}/history", response_model=List[HistoryEvent], status_code=status.HTTP_200_OK)
async def get_history(
    userId: str,
    service: HistoryService = Depends(get_history_service)
) -> List[HistoryEvent]:
    return await service.get_history(userId)

@router.get("/{userId}/analytics", response_model=Analytics, status_code=status.HTTP_200_OK)
async def get_analytics(
    userId: str,
    service: AnalyticsService = Depends(get_analytics_service)
) -> Analytics:
    return await service.get_analytics(userId)

@router.get("/{userId}/agent-runs", response_model=AgentPipeline, status_code=status.HTTP_200_OK)
async def get_agent_runs(
    userId: str,
    service: AgentService = Depends(get_agent_service)
) -> AgentPipeline:
    return await service.get_agent_runs(userId)

@router.get("/{userId}/settings", response_model=UserSettings, status_code=status.HTTP_200_OK)
async def get_settings(
    userId: str,
    service: UserService = Depends(get_user_service)
) -> UserSettings:
    return await service.get_settings(userId)

@router.put("/{userId}/settings", response_model=UserSettings, status_code=status.HTTP_200_OK)
async def update_settings(
    userId: str,
    settings: UserSettings,
    service: UserService = Depends(get_user_service)
) -> UserSettings:
    return await service.update_settings(userId, settings)

@router.get("/{userId}/recommendations", response_model=List[Recommendation], status_code=status.HTTP_200_OK)
async def get_user_recommendations(
    userId: str,
    service: RecommendationService = Depends(get_recommendation_service)
) -> List[Recommendation]:
    return await service.get_user_recommendations(userId)

@router.get("/{userId}/rejected", response_model=List[RejectedContent], status_code=status.HTTP_200_OK)
async def get_rejected_content(
    userId: str,
    service: RecommendationService = Depends(get_recommendation_service)
) -> List[RejectedContent]:
    return await service.get_rejected_content(userId)
