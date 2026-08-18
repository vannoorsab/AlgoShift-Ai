from typing import List, Dict, Any, Union
from fastapi import APIRouter, Depends, status
from app.models.interest import Interest, InterestInference, InterestGraph, InterestProfile
from app.services.interest_service import InterestService

router = APIRouter(prefix="/users", tags=["Interests"])

def get_interest_service() -> InterestService:
    return InterestService()

@router.get("/{userId}/interests", response_model=Union[InterestProfile, List[Interest]], status_code=status.HTTP_200_OK)
async def get_interests(
    userId: str,
    service: InterestService = Depends(get_interest_service)
):
    profile = await service.infer_interests(userId)
    return profile

@router.get("/{userId}/interest-inference", response_model=InterestInference, status_code=status.HTTP_200_OK)
async def get_interest_inference(
    userId: str,
    service: InterestService = Depends(get_interest_service)
) -> InterestInference:
    return await service.get_user_inference(userId)

@router.get("/{userId}/interest-graph", response_model=InterestGraph, status_code=status.HTTP_200_OK)
async def get_interest_graph(
    userId: str,
    service: InterestService = Depends(get_interest_service)
) -> InterestGraph:
    return await service.get_user_graph(userId)

@router.get("/{userId}/interest-timeline", status_code=status.HTTP_200_OK)
async def get_interest_timeline(
    userId: str,
    service: InterestService = Depends(get_interest_service)
) -> List[Dict[str, Any]]:
    return await service.get_user_timeline(userId)
