import pytest

@pytest.mark.asyncio
async def test_record_interaction(client):
    payload = {
        "reelId": "r1",
        "type": "like",
        "timestamp": "2026-08-18T10:00:00Z"
    }
    response = await client.post("/api/interactions", json=payload)
    assert response.status_code == 200
    assert response.json() == {"ok": True}
