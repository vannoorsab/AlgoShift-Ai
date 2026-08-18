from typing import Dict, Any, Optional
from app.repositories.interaction_repository import InteractionRepository
from app.models.interaction import Interaction

class InteractionService:
    def __init__(self, interaction_repo: Optional[InteractionRepository] = None):
        self.repo = interaction_repo or InteractionRepository()

    async def record_interaction(self, interaction: Interaction, user_id: str = "demo-user") -> bool:
        data = interaction.model_dump()
        data["userId"] = user_id
        await self.repo.record(data)
        return True
