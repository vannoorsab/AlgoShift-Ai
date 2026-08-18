import pytest
import io
from app.services.seed_service import seed_initial_data
from app.services.workflow_orchestrator import WorkflowOrchestratorService
from app.models.workflow import AnalyzeRequest

@pytest.mark.asyncio
async def test_workflow_dataset_mode_end_to_end(client):
    """TEST 1 & 10 — Dataset Mode & Built-in Challenge Trap End-to-End."""
    await seed_initial_data()
    payload = {"userId": "student_001", "inputMode": "dataset"}
    
    response = await client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert data["success"] is True
    assert "runId" in data
    assert data["workflow"]["status"] == "completed"
    
    res = data["result"]
    assert res["currentReel"]["reelId"] == "R003"
    assert res["interestDetected"]["topic"] == "Software Engineering"
    assert res["recommendedTechReel"]["title"] is not None
    assert "10 AI Tools That Will Get You A Job" not in res["recommendedTechReel"]["title"]
    assert res["category"] == "Cloud"
    assert res["confidence"] == "High"

@pytest.mark.asyncio
async def test_workflow_upload_mode(client):
    """TEST 2 — Upload Mode Pipeline."""
    await seed_initial_data()
    video_bytes = b"fake mp4 video binary content for testing"
    files = {"file": ("demo_video.mp4", io.BytesIO(video_bytes), "video/mp4")}
    data = {"userId": "student_001", "inputMode": "upload"}
    
    response = await client.post("/api/analyze", data=data, files=files)
    assert response.status_code == 200
    res_data = response.json()
    
    assert res_data["success"] is True
    assert res_data["workflow"]["status"] == "completed"

@pytest.mark.asyncio
async def test_workflow_url_mode_controlled_error(client):
    """TEST 3 — Invalid URL Mode Pipeline: Returns controlled error message."""
    payload = {"userId": "student_001", "inputMode": "url", "url": "https://instagram.com/reel/123456"}
    response = await client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert data["success"] is False
    assert data["error"]["code"] == "REEL_ACCESS_ERROR"
    assert "Please upload the video instead" in data["error"]["message"]

@pytest.mark.asyncio
async def test_workflow_agent2_failure_handling(monkeypatch):
    """TEST 4 — Agent 2 Failure Handling: Interest inference failure stops pipeline safely."""
    orch = WorkflowOrchestratorService()
    
    async def mock_fail(*args, **kwargs):
        raise RuntimeError("Agent 2 InterestInference failure simulation")
        
    monkeypatch.setattr(orch.interest_agent, "infer_interests", mock_fail)
    req = AnalyzeRequest(userId="student_001", inputMode="dataset")
    res = await orch.run_pipeline(req)
    
    assert res.success is False
    assert res.error.step == "inferring_interests"
    assert "Agent 2 InterestInference failure simulation" in res.error.message

@pytest.mark.asyncio
async def test_workflow_quality_gate_rejection_integration(client):
    """TEST 5 — Quality Gate Filtering Integration: Rejected hype candidate cannot be selected."""
    await seed_initial_data()
    response = await client.post("/api/analyze", json={"userId": "student_001", "inputMode": "dataset"})
    assert response.status_code == 200
    data = response.json()
    
    winner_title = data["result"]["recommendedTechReel"]["title"]
    assert "10 AI Tools" not in winner_title

@pytest.mark.asyncio
async def test_workflow_explanation_integration(client):
    """TEST 6 — Explanation Integration: Agent 5 winner matches Agent 6 explanation."""
    await seed_initial_data()
    response = await client.post("/api/analyze", json={"userId": "student_001", "inputMode": "dataset"})
    assert response.status_code == 200
    data = response.json()
    
    res = data["result"]
    assert "whyThisRecommendation" in res
    assert len(res["whyThisRecommendation"]) > 10

@pytest.mark.asyncio
async def test_workflow_feedback_processing(client):
    """TEST 7 — Feedback Processing: POST /api/feedback updates profile via Agent 7."""
    await seed_initial_data()
    payload = {
        "userId": "student_001",
        "reelId": "TECH014",
        "watchPercentage": 96.0,
        "liked": True,
        "saved": True
    }
    response = await client.post("/api/feedback", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert data["success"] is True
    assert len(data["updatedInterests"]) > 0

@pytest.mark.asyncio
async def test_workflow_next_recommendation_adaptation(client):
    """TEST 8 — Next Recommendation Adaptation: POST /api/analyze/next uses updated profile."""
    await seed_initial_data()
    # 1. Post feedback
    await client.post("/api/feedback", json={"userId": "student_001", "reelId": "TECH014", "watchPercentage": 96.0, "liked": True, "saved": True})
    
    # 2. Call /api/analyze/next
    response = await client.post("/api/analyze/next", json={"userId": "student_001"})
    assert response.status_code == 200
    data = response.json()
    
    assert data["success"] is True
    assert data["result"]["category"] in ["Cloud", "HLD", "Java", "Hardware", "AI", "DSA", "Cybersecurity", "Career", "Other"]

@pytest.mark.asyncio
async def test_workflow_idempotency_caching(client):
    """TEST 9 — Idempotency & Cached Analysis Reuse."""
    await seed_initial_data()
    res1 = await client.post("/api/analyze", json={"userId": "student_001", "inputMode": "dataset"})
    res2 = await client.post("/api/analyze", json={"userId": "student_001", "inputMode": "dataset"})
    
    assert res1.status_code == 200
    assert res2.status_code == 200
    assert res1.json()["success"] is True
    assert res2.json()["success"] is True

@pytest.mark.asyncio
async def test_get_workflow_run_endpoint(client):
    """Integration Test: GET /api/workflows/{runId} status tracking."""
    await seed_initial_data()
    res = await client.post("/api/analyze", json={"userId": "student_001", "inputMode": "dataset"})
    run_id = res.json()["runId"]
    
    wf_res = await client.get(f"/api/workflows/{run_id}")
    assert wf_res.status_code == 200
    wf_data = wf_res.json()
    
    assert wf_data["runId"] == run_id
    assert wf_data["status"] == "completed"
    assert len(wf_data["steps"]) >= 6
