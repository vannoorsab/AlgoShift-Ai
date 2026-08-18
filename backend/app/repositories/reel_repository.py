import datetime
from typing import Optional, Dict, Any, List
from app.repositories.base_repository import BaseRepository
from app.db.mongodb import COLLECTION_REELS
from app.models.reel import ReelContent, ReelAnalysis

class ReelRepository(BaseRepository):
    def __init__(self, db=None):
        super().__init__(COLLECTION_REELS, db)

    async def get_by_id(self, reel_id: str) -> Optional[Dict[str, Any]]:
        return await self.find_one({"reelId": reel_id})

    async def save_reel_record(self, content: ReelContent, analysis: ReelAnalysis) -> Dict[str, Any]:
        now = datetime.datetime.utcnow().isoformat() + "Z"
        existing = await self.get_by_id(content.reelId)
        
        record = {
            "reelId": content.reelId,
            "sourceType": content.sourceType.value if hasattr(content.sourceType, 'value') else str(content.sourceType),
            "sourceUrl": content.sourceUrl,
            "content": content.model_dump(),
            "analysis": analysis.model_dump(),
            "analysisVersion": "1.0",
            "createdAt": existing.get("createdAt", now) if existing else now,
            "updatedAt": now
        }
        
        await self.update_one({"reelId": content.reelId}, record, upsert=True)
        return record
