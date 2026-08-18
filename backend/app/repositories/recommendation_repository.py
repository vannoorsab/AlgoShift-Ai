from typing import Optional, Dict, Any, List
from app.repositories.base_repository import BaseRepository
from app.db.mongodb import COLLECTION_RECOMMENDATIONS, COLLECTION_FEEDBACK

class RecommendationRepository:
    def __init__(self, db=None):
        self.recs_repo = BaseRepository(COLLECTION_RECOMMENDATIONS, db)
        self.recommendations_repo = self.recs_repo
        self.feedback_repo = BaseRepository(COLLECTION_FEEDBACK, db)

    async def get_by_user(self, user_id: str) -> List[Dict[str, Any]]:
        return await self.recs_repo.find_many({"userId": user_id})

    async def get_user_recommendations(self, user_id: str) -> List[Dict[str, Any]]:
        return await self.get_by_user(user_id)

    async def get_by_id(self, rec_id: str) -> Optional[Dict[str, Any]]:
        return await self.recs_repo.find_one({"id": rec_id})

    async def save_recommendation(self, rec_data: Dict[str, Any]) -> Dict[str, Any]:
        await self.recs_repo.update_one({"id": rec_data["id"]}, rec_data, upsert=True)
        return rec_data

    async def save_feedback(self, rec_id: str, feedback: str, reason: Optional[str] = None) -> bool:
        doc = {"recommendationId": rec_id, "feedback": feedback}
        if reason:
            doc["reason"] = reason
        await self.feedback_repo.insert_one(doc)
        await self.recs_repo.update_one({"id": rec_id}, {"feedback": feedback})
        return True

    async def get_rejected(self, user_id: str) -> List[Dict[str, Any]]:
        return await self.recs_repo.find_many({"userId": user_id, "status": "REJECTED"})
