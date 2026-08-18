from typing import Optional, Dict, Any
from app.repositories.base_repository import BaseRepository
from app.db.mongodb import COLLECTION_USERS

class UserRepository(BaseRepository):
    def __init__(self, db=None):
        super().__init__(COLLECTION_USERS, db)

    async def get_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        return await self.find_one({"id": user_id})

    async def get_settings(self, user_id: str) -> Optional[Dict[str, Any]]:
        doc = await self.get_by_id(user_id)
        return doc.get("settings") if doc else None

    async def update_settings(self, user_id: str, settings_dict: Dict[str, Any]) -> bool:
        return await self.update_one({"id": user_id}, {"settings": settings_dict})
