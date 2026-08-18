from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, status, Body, UploadFile, File, Form
from app.models.reel import AnalyzeReelResponse, AnalyzeReelRequest
from app.services.reel_service import ReelService
from app.core.errors import EntityNotFoundException, ValidationException

router = APIRouter(prefix="/reels", tags=["Reels"])

def get_reel_service() -> ReelService:
    return ReelService()

@router.post("/analyze", response_model=AnalyzeReelResponse, status_code=status.HTTP_200_OK)
async def analyze_reel(
    payload: Dict[str, Any] = Body(...),
    service: ReelService = Depends(get_reel_service)
) -> AnalyzeReelResponse:
    """Existing endpoint analyzing normalized Reel content."""
    return await service.analyze_reel(payload)

@router.post("/upload", response_model=AnalyzeReelResponse, status_code=status.HTTP_200_OK)
async def upload_reel(
    file: UploadFile = File(...),
    service: ReelService = Depends(get_reel_service)
) -> AnalyzeReelResponse:
    """Source 2: Upload endpoint for .mp4/.mov video files."""
    contents = await file.read()
    filename = file.filename or "uploaded_video.mp4"
    content_type = file.content_type
    
    normalized_content = await service.ingestion_service.ingest_upload(contents, filename, content_type)
    return await service.analyze_reel(normalized_content.model_dump())

@router.post("/analyze-url", response_model=AnalyzeReelResponse, status_code=status.HTTP_200_OK)
async def analyze_url(
    payload: Dict[str, Any] = Body(...),
    service: ReelService = Depends(get_reel_service)
) -> AnalyzeReelResponse:
    """Source 3: URL endpoint (returns controlled error if unretrievable)."""
    url = payload.get("url") or payload.get("sourceUrl") or ""
    normalized_content = await service.ingestion_service.ingest_url(url)
    return await service.analyze_reel(normalized_content.model_dump())

@router.post("/analyze-dataset", response_model=AnalyzeReelResponse, status_code=status.HTTP_200_OK)
async def analyze_dataset(
    payload: Dict[str, Any] = Body(...),
    service: ReelService = Depends(get_reel_service)
) -> AnalyzeReelResponse:
    """Source 1: Dataset endpoint loading anonymized challenge Reels."""
    reel_id = payload.get("reelId", "R001")
    normalized_content = await service.ingestion_service.ingest_dataset(reel_id, payload)
    return await service.analyze_reel(normalized_content.model_dump())

@router.get("/{reelId}", status_code=status.HTTP_200_OK)
async def get_reel_record(
    reelId: str,
    service: ReelService = Depends(get_reel_service)
):
    record = await service.get_reel_by_id(reelId)
    if not record:
        raise EntityNotFoundException("ReelRecord", reelId)
    return record
