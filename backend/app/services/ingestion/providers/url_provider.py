from typing import Dict, Any
from app.services.ingestion.provider_interface import ReelIngestionProvider
from app.models.reel import NormalizedReelContent
from app.core.errors import ValidationException

class URLProvider(ReelIngestionProvider):
    """Source 3: URLProvider abstraction."""

    async def fetch(self, content_input: Dict[str, Any]) -> NormalizedReelContent:
        url = content_input.get("sourceUrl") or content_input.get("url") or ""
        # Return clear controlled error without faking URL extraction or bypassing auth
        raise ValidationException(
            message="Unable to retrieve Reel content from this URL. Please upload the video instead.",
            details={"url": url, "sourceType": "url"}
        )
