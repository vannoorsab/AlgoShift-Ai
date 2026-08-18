from typing import Any, Dict, List, Optional
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
from app.db.mongodb import get_database

class BaseRepository:
    def __init__(self, collection_name: str, db: Optional[AsyncIOMotorDatabase] = None):
        self.collection_name = collection_name
        self._db = db

    @property
    def collection(self) -> AsyncIOMotorCollection:
        db = self._db if self._db is not None else get_database()
        return db[self.collection_name]

    async def find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return await self.collection.find_one(query, {"_id": 0})

    async def find_many(self, query: Dict[str, Any] = None, limit: int = 100) -> List[Dict[str, Any]]:
        cursor = self.collection.find(query or {}, {"_id": 0}).limit(limit)
        return await cursor.to_list(length=limit)

    async def insert_one(self, data: Dict[str, Any]) -> Dict[str, Any]:
        await self.collection.insert_one(data)
        data.pop("_id", None)
        return data

    async def update_one(self, query: Dict[str, Any], update: Dict[str, Any], upsert: bool = True) -> bool:
        result = await self.collection.update_one(query, {"$set": update}, upsert=upsert)
        return result.modified_count > 0 or result.upserted_id is not None

    async def delete_one(self, query: Dict[str, Any]) -> bool:
        result = await self.collection.delete_one(query)
        return result.deleted_count > 0
