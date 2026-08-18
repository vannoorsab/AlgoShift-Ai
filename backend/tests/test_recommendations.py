import pytest

@pytest.mark.asyncio
async def test_generate_and_get_recommendations(client):
    gen_response = await client.post("/api/recommendations/generate", json={"userId": "demo-user"})
    assert gen_response.status_code == 200
    recs = gen_response.json()
    assert isinstance(recs, list)
    assert len(recs) > 0

    get_response = await client.get("/api/users/demo-user/recommendations")
    assert get_response.status_code == 200
    assert len(get_response.json()) > 0

@pytest.mark.asyncio
async def test_send_feedback(client):
    response = await client.post("/api/recommendations/rec1/feedback", json={"feedback": "useful"})
    assert response.status_code == 200
    assert response.json() == {"ok": True}

@pytest.mark.asyncio
async def test_get_rejected(client):
    response = await client.get("/api/users/demo-user/rejected")
    assert response.status_code == 200
    rejected = response.json()
    assert isinstance(rejected, list)
    assert len(rejected) > 0
    assert rejected[0]["status"] == "REJECTED"
