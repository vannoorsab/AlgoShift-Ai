from typing import Dict, Any
from app.services.ingestion.provider_interface import ReelIngestionProvider
from app.models.reel import ReelContent, SourceType

class UploadIngestionProvider(ReelIngestionProvider):
    async def fetch(self, content_input: Dict[str, Any]) -> ReelContent:
        return ReelContent(
            reelId=content_input.get("reelId", "UPLOADING"),
            sourceType=SourceType.UPLOAD,
            sourceUrl=content_input.get("sourceUrl"),
            title=content_input.get("title", "Uploaded Video"),
            caption=content_input.get("caption", ""),
            hashtags=content_input.get("hashtags", []),
            transcript=content_input.get("transcript", ""),
            visualDescription=content_input.get("visualDescription", ""),
            ocrText=content_input.get("ocrText", "")
        )
