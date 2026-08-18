from typing import Dict, Any
from app.services.ingestion.provider_interface import ReelIngestionProvider
from app.services.demo_dataset import get_demo_reel, DEMO_REELS
from app.models.reel import NormalizedReelContent, SourceType

class DatasetProvider(ReelIngestionProvider):
    """Source 1: DatasetProvider loading anonymized challenge dataset Reels."""
    
    async def fetch(self, content_input: Dict[str, Any]) -> NormalizedReelContent:
        reel_id = content_input.get("reelId", "R001")
        
        # Look up in DEMO_REELS
        if reel_id in DEMO_REELS and not content_input.get("title"):
            base_reel = get_demo_reel(reel_id)
            return NormalizedReelContent(
                reelId=base_reel.reelId,
                sourceType=SourceType.DEMO,
                sourceUrl=base_reel.sourceUrl,
                title=base_reel.title,
                caption=base_reel.caption,
                hashtags=base_reel.hashtags,
                transcript=base_reel.transcript,
                ocrText=base_reel.ocrText,
                visualDescription=base_reel.visualDescription,
                mediaMetadata={"provider": "DatasetProvider", "datasetId": reel_id}
            )

        return NormalizedReelContent(
            reelId=reel_id,
            sourceType=SourceType.DEMO,
            sourceUrl=content_input.get("sourceUrl"),
            title=content_input.get("title") or "Dataset Reel",
            caption=content_input.get("caption") or "",
            hashtags=content_input.get("hashtags") or [],
            transcript=content_input.get("transcript") or "",
            ocrText=content_input.get("ocrText") or "",
            visualDescription=content_input.get("visualDescription") or "",
            mediaMetadata={"provider": "DatasetProvider", "datasetId": reel_id}
        )
