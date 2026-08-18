from typing import List, Dict, Any, Optional
from app.repositories.base_repository import BaseRepository
from app.db.mongodb import COLLECTION_RECOMMENDATION_CATALOG
from app.services.catalog_dataset import CATALOG_ITEMS

class CatalogRepository:
    def __init__(self, db=None):
        self.catalog_repo = BaseRepository(COLLECTION_RECOMMENDATION_CATALOG, db)

    async def get_all_items(self) -> List[Dict[str, Any]]:
        items = await self.catalog_repo.find_many({})
        if items and len(items) > 0:
            return items
        return CATALOG_ITEMS

    async def find_by_topics(self, topics: List[str]) -> List[Dict[str, Any]]:
        all_items = await self.get_all_items()
        matched = []
        for item in all_items:
            item_topics = [t.lower() for t in item.get("topics", [])] + [item.get("topic", "").lower()]
            if any(tp.lower() in item_topics for tp in topics):
                matched.append(item)
        return matched if matched else all_items
