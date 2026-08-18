from typing import Dict, Any, Optional
from app.models.reel import NormalizedReelContent, SourceType
from app.services.ingestion.providers.dataset_provider import DatasetProvider
from app.services.ingestion.providers.upload_provider import UploadProvider
from app.services.ingestion.providers.url_provider import URLProvider

class ReelIngestionService:
    """
    ReelIngestionService:
    Coordinates DatasetProvider, UploadProvider, and URLProvider to produce NormalizedReelContent.
    """
    def __init__(
        self,
        dataset_provider: Optional[DatasetProvider] = None,
        upload_provider: Optional[UploadProvider] = None,
        url_provider: Optional[URLProvider] = None
    ):
        self.dataset_provider = dataset_provider or DatasetProvider()
        self.upload_provider = upload_provider or UploadProvider()
        self.url_provider = url_provider or URLProvider()

    async def ingest_dataset(self, reel_id: str = "R001", extra_data: Dict[str, Any] = None) -> NormalizedReelContent:
        data = extra_data or {}
        data["reelId"] = reel_id
        data["sourceType"] = SourceType.DEMO
        return await self.dataset_provider.fetch(data)

    async def ingest_upload(
        self,
        file_bytes: bytes,
        filename: str,
        content_type: Optional[str] = None
    ) -> NormalizedReelContent:
        return await self.upload_provider.process_file(file_bytes, filename, content_type)

    async def ingest_url(self, url: str) -> NormalizedReelContent:
        return await self.url_provider.fetch({"sourceUrl": url, "sourceType": SourceType.URL})

    async def ingest(self, content_input: Dict[str, Any]) -> NormalizedReelContent:
        st_raw = str(content_input.get("sourceType", "demo")).lower()
        if st_raw == "upload":
            return await self.upload_provider.fetch(content_input)
        elif st_raw == "url":
            return await self.url_provider.fetch(content_input)
        else:
            return await self.dataset_provider.fetch(content_input)
