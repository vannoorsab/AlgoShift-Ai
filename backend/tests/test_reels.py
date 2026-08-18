import pytest

@pytest.mark.asyncio
async def test_analyze_reel(client):
    payload = {"reelId": "R001", "sourceType": "demo", "title": "Java Developers at 2 AM"}
    response = await client.post("/api/reels/analyze", json=payload)
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["success"] is True
    analysis = res_data["analysis"]
    assert "primaryTopic" in analysis
    assert "educationalValue" in analysis
    assert "hypeScore" in analysis
    assert "difficulty" in analysis
    assert "confidence" in analysis
