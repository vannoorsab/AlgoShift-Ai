from typing import List, Dict, Any
from app.repositories.base_repository import BaseRepository
from app.db.mongodb import COLLECTION_INTERACTIONS

class InteractionRepository(BaseRepository):
    def __init__(self, db=None):
        super().__init__(COLLECTION_INTERACTIONS, db)

    async def record(self, interaction_data: Dict[str, Any]) -> Dict[str, Any]:
        return await self.insert_one(interaction_data)

    async def get_by_user(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        return await self.find_many({"userId": user_id}, limit=limit)
