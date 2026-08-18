from abc import ABC, abstractmethod
from typing import Dict, Any
from app.models.reel import ReelContent

class ReelIngestionProvider(ABC):
    @abstractmethod
    async def fetch(self, content_input: Dict[str, Any]) -> ReelContent:
        """Fetch and normalize reel content from the underlying source."""
        pass
