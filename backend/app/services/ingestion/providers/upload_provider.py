import os
import uuid
import datetime
from typing import Dict, Any, Optional
from app.services.ingestion.provider_interface import ReelIngestionProvider
from app.services.ingestion.adapters.transcription_adapter import TranscriptionAdapter, MockWhisperTranscriptionAdapter
from app.services.ingestion.adapters.ocr_adapter import OCRAdapter, MockTesseractOCRAdapter
from app.services.ingestion.adapters.vision_adapter import VisualAnalysisAdapter, MockVisionAdapter
from app.models.reel import NormalizedReelContent, SourceType
from app.core.errors import ValidationException
from app.core.logging import logger

ALLOWED_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}
MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "uploads")

class UploadProvider(ReelIngestionProvider):
    """Source 2: UploadProvider for uploaded video files (.mp4/.mov)."""

    def __init__(
        self,
        transcription_adapter: Optional[TranscriptionAdapter] = None,
        ocr_adapter: Optional[OCRAdapter] = None,
        vision_adapter: Optional[VisualAnalysisAdapter] = None
    ):
        self.transcription_adapter = transcription_adapter or MockWhisperTranscriptionAdapter()
        self.ocr_adapter = ocr_adapter or MockTesseractOCRAdapter()
        self.vision_adapter = vision_adapter or MockVisionAdapter()

    async def process_file(
        self,
        file_bytes: bytes,
        filename: str,
        content_type: Optional[str] = None
    ) -> NormalizedReelContent:
        # 1. Validate file extension
        ext = os.path.splitext(filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise ValidationException(
                message=f"Unsupported file type '{ext}'. Please upload an .mp4, .mov, or valid video file.",
                details={"filename": filename, "allowed": list(ALLOWED_EXTENSIONS)}
            )

        # 2. Validate file size
        file_size = len(file_bytes)
        if file_size > MAX_FILE_SIZE_BYTES:
            raise ValidationException(
                message=f"File size ({file_size / (1024*1024):.1f} MB) exceeds maximum limit of 50 MB.",
                details={"filename": filename, "sizeBytes": file_size, "maxBytes": MAX_FILE_SIZE_BYTES}
            )

        # 3. Store file safely
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        safe_filename = f"{uuid.uuid4().hex}_{os.path.basename(filename)}"
        saved_file_path = os.path.join(UPLOAD_DIR, safe_filename)

        with open(saved_file_path, "wb") as f:
            f.write(file_bytes)

        logger.info(f"UploadProvider saved file safely to {saved_file_path}")

        # 4. Extract audio & generate transcript
        transcript = await self.transcription_adapter.transcribe(saved_file_path)

        # 5. Sample video frames & extract OCR text
        ocr_text = await self.ocr_adapter.extract_ocr(saved_file_path)

        # 6. Generate visual description
        visual_desc = await self.vision_adapter.describe_visuals(saved_file_path)

        # 7. Build NormalizedReelContent
        reel_id = f"UPL_{uuid.uuid4().hex[:8]}"
        
        media_metadata = {
            "provider": "UploadProvider",
            "originalFilename": filename,
            "savedFilePath": saved_file_path,
            "fileSizeBytes": file_size,
            "mimeType": content_type or f"video/{ext.replace('.', '')}",
            "processedAt": datetime.datetime.utcnow().isoformat() + "Z"
        }

        return NormalizedReelContent(
            reelId=reel_id,
            sourceType=SourceType.UPLOAD,
            sourceUrl=saved_file_path,
            title=f"Uploaded Reel ({filename})",
            caption=f"Uploaded video content {filename}",
            hashtags=["upload", "video"],
            transcript=transcript,
            ocrText=ocr_text,
            visualDescription=visual_desc,
            mediaMetadata=media_metadata
        )

    async def fetch(self, content_input: Dict[str, Any]) -> NormalizedReelContent:
        file_bytes = content_input.get("file_bytes")
        filename = content_input.get("filename", "video.mp4")
        content_type = content_input.get("content_type")

        if file_bytes:
            return await self.process_file(file_bytes, filename, content_type)

        # Fallback if raw text payload passed
        return NormalizedReelContent(
            reelId=content_input.get("reelId", f"UPL_{uuid.uuid4().hex[:8]}"),
            sourceType=SourceType.UPLOAD,
            sourceUrl=content_input.get("sourceUrl"),
            title=content_input.get("title", "Uploaded Reel"),
            caption=content_input.get("caption", ""),
            hashtags=content_input.get("hashtags", []),
            transcript=content_input.get("transcript", "Sample uploaded video transcript."),
            ocrText=content_input.get("ocrText", "SAMPLE OCR"),
            visualDescription=content_input.get("visualDescription", "Sample video visual description."),
            mediaMetadata={"provider": "UploadProvider"}
        )
