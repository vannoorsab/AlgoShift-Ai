import pytest

@pytest.mark.asyncio
async def test_get_interests(client):
    response = await client.get("/api/users/demo-user/interests")
    assert response.status_code == 200
    interests = response.json()
    if isinstance(interests, dict):
        assert "primaryInterests" in interests
        assert "curiosity" in interests
    else:
        assert isinstance(interests, list)

@pytest.mark.asyncio
async def test_get_interest_inference(client):
    response = await client.get("/api/users/demo-user/interest-inference")
    assert response.status_code == 200
    data = response.json()
    assert "primaryInterest" in data
    assert "supportingSignals" in data

@pytest.mark.asyncio
async def test_get_interest_graph(client):
    response = await client.get("/api/users/demo-user/interest-graph")
    assert response.status_code == 200
    data = response.json()
    assert "root" in data
    assert "nodes" in data
    assert "edges" in data
