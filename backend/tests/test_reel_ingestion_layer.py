import pytest
import io
from app.services.ingestion.service import ReelIngestionService
from app.models.reel import SourceType
from app.core.errors import ValidationException

@pytest.mark.asyncio
async def test_dataset_provider_ingestion():
    service = ReelIngestionService()
    content = await service.ingest_dataset("R001")
    
    assert content.reelId == "R001"
    assert content.sourceType == SourceType.DEMO
    assert content.title == "Java Developers at 2 AM"
    assert "transcript" in content.model_dump()
    assert content.mediaMetadata["provider"] == "DatasetProvider"

@pytest.mark.asyncio
async def test_upload_provider_valid_video():
    service = ReelIngestionService()
    dummy_video_bytes = b"\x00\x00\x00\x18ftypmp42\x00\x00\x00\x00mp41isom"
    filename = "sample_test_video.mp4"
    
    content = await service.ingest_upload(dummy_video_bytes, filename, "video/mp4")
    
    assert content.sourceType == SourceType.UPLOAD
    assert filename in content.title
    assert "Transcript" in content.transcript or "transcript" in content.transcript.lower()
    assert "OCR" in content.ocrText
    assert "Visual Description" in content.visualDescription
    assert content.mediaMetadata["originalFilename"] == filename

@pytest.mark.asyncio
async def test_upload_provider_invalid_extension():
    service = ReelIngestionService()
    dummy_bytes = b"Hello world text file"
    filename = "malicious_script.exe"
    
    with pytest.raises(ValidationException) as exc_info:
        await service.ingest_upload(dummy_bytes, filename, "application/octet-stream")
        
    assert "Unsupported file type" in str(exc_info.value)

@pytest.mark.asyncio
async def test_url_provider_controlled_error():
    service = ReelIngestionService()
    url = "https://instagram.com/reel/unknown"
    
    with pytest.raises(ValidationException) as exc_info:
        await service.ingest_url(url)
        
    assert "Unable to retrieve Reel content from this URL. Please upload the video instead." in str(exc_info.value)

@pytest.mark.asyncio
async def test_api_analyze_dataset_endpoint(client):
    response = await client.post("/api/reels/analyze-dataset", json={"reelId": "R001"})
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["success"] is True
    assert res_data["analysis"]["primaryTopic"] == "Java"

@pytest.mark.asyncio
async def test_api_upload_endpoint(client):
    dummy_video_bytes = b"\x00\x00\x00\x18ftypmp42\x00\x00\x00\x00mp41isom"
    files = {"file": ("demo_clip.mp4", io.BytesIO(dummy_video_bytes), "video/mp4")}
    
    response = await client.post("/api/reels/upload", files=files)
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["success"] is True
    assert "primaryTopic" in res_data["analysis"]

@pytest.mark.asyncio
async def test_api_analyze_url_controlled_error_endpoint(client):
    response = await client.post("/api/reels/analyze-url", json={"url": "https://instagram.com/reel/abc"})
    assert response.status_code == 422
    err_data = response.json()
    assert "Unable to retrieve Reel content from this URL. Please upload the video instead." in err_data["message"]
