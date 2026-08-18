from typing import Optional, Dict, Any, List
from app.repositories.base_repository import BaseRepository
from app.db.mongodb import COLLECTION_AGENT_RUNS

class AgentRunRepository(BaseRepository):
    def __init__(self, db=None):
        super().__init__(COLLECTION_AGENT_RUNS, db)

    async def get_latest_by_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        runs = await self.find_many({"userId": user_id}, limit=1)
        return runs[0] if runs else None

    async def save_pipeline_run(self, pipeline_data: Dict[str, Any]) -> Dict[str, Any]:
        await self.update_one({"runId": pipeline_data["runId"]}, pipeline_data, upsert=True)
        return pipeline_data
