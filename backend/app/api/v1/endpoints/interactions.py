from fastapi import APIRouter, Depends, status
from app.models.interaction import Interaction
from app.services.interaction_service import InteractionService

router = APIRouter(prefix="/interactions", tags=["Interactions"])

def get_interaction_service() -> InteractionService:
    return InteractionService()

@router.post("", status_code=status.HTTP_200_OK)
async def record_interaction(
    interaction: Interaction,
    service: InteractionService = Depends(get_interaction_service)
):
    await service.record_interaction(interaction)
    return {"ok": True}
