import datetime
from typing import Optional, Dict, Any, List
from app.repositories.base_repository import BaseRepository
from app.db.mongodb import COLLECTION_INTEREST_PROFILES, COLLECTION_INTEREST_GRAPH, COLLECTION_INTEREST_HISTORY

class InterestRepository:
    def __init__(self, db=None):
        self.profiles_repo = BaseRepository(COLLECTION_INTEREST_PROFILES, db)
        self.graph_repo = BaseRepository(COLLECTION_INTEREST_GRAPH, db)
        self.history_repo = BaseRepository(COLLECTION_INTEREST_HISTORY, db)

    async def get_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        return await self.profiles_repo.find_one({"userId": user_id})

    async def save_profile(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        user_id = profile_data["userId"]
        now = datetime.datetime.utcnow().isoformat() + "Z"
        profile_data["updatedAt"] = now
        
        # Save current profile to interest_profiles
        await self.profiles_repo.update_one({"userId": user_id}, profile_data, upsert=True)
        
        # Save snapshot into interest_history
        history_entry = {
            "userId": user_id,
            "timestamp": now,
            "profileSnapshot": profile_data
        }
        await self.history_repo.insert_one(history_entry)
        
        return profile_data

    async def get_interests(self, user_id: str) -> List[Dict[str, Any]]:
        return await self.profiles_repo.find_many({"userId": user_id})

    async def get_inference(self, user_id: str) -> Optional[Dict[str, Any]]:
        doc = await self.graph_repo.find_one({"userId": user_id})
        if doc and "inference" in doc:
            return doc["inference"]
        return None

    async def get_graph(self, user_id: str) -> Optional[Dict[str, Any]]:
        return await self.graph_repo.find_one({"userId": user_id})

    async def get_timeline(self, user_id: str) -> List[Dict[str, Any]]:
        return await self.history_repo.find_many({"userId": user_id})
