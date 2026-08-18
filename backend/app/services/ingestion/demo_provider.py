from typing import Dict, Any
from app.services.ingestion.provider_interface import ReelIngestionProvider
from app.services.demo_dataset import get_demo_reel, DEMO_REELS
from app.models.reel import ReelContent

class DemoIngestionProvider(ReelIngestionProvider):
    async def fetch(self, content_input: Dict[str, Any]) -> ReelContent:
        reel_id = content_input.get("reelId", "R001")
        
        # If user passed custom title/transcript, override demo defaults
        if reel_id in DEMO_REELS and not content_input.get("title"):
            return get_demo_reel(reel_id)
            
        return ReelContent(
            reelId=reel_id,
            sourceType=content_input.get("sourceType", "demo"),
            sourceUrl=content_input.get("sourceUrl"),
            title=content_input.get("title") or get_demo_reel(reel_id).title,
            caption=content_input.get("caption") or get_demo_reel(reel_id).caption,
            hashtags=content_input.get("hashtags") or get_demo_reel(reel_id).hashtags,
            transcript=content_input.get("transcript") or get_demo_reel(reel_id).transcript,
            visualDescription=content_input.get("visualDescription") or get_demo_reel(reel_id).visualDescription,
            ocrText=content_input.get("ocrText") or get_demo_reel(reel_id).ocrText,
        )
