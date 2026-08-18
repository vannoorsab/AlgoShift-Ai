from typing import Dict, Any
from app.services.ingestion.provider_interface import ReelIngestionProvider
from app.models.reel import ReelContent
from app.core.errors import ValidationException

class UrlIngestionProvider(ReelIngestionProvider):
    async def fetch(self, content_input: Dict[str, Any]) -> ReelContent:
        url = content_input.get("sourceUrl") or content_input.get("url") or ""
        raise ValidationException(
            message="Unable to retrieve Reel content from this URL. Please upload the video or use a supported source.",
            details={"url": url, "sourceType": "url"}
        )
