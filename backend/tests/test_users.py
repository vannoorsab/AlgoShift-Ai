import pytest

@pytest.mark.asyncio
async def test_get_history(client):
    response = await client.get("/api/users/demo-user/history")
    assert response.status_code == 200
    history = response.json()
    assert isinstance(history, list)

@pytest.mark.asyncio
async def test_get_analytics(client):
    response = await client.get("/api/users/demo-user/analytics")
    assert response.status_code == 200
    analytics = response.json()
    assert "kpis" in analytics
    assert "interestEvolution" in analytics

@pytest.mark.asyncio
async def test_get_agent_runs(client):
    response = await client.get("/api/users/demo-user/agent-runs")
    assert response.status_code == 200
    runs = response.json()
    assert "runId" in runs
    assert "agents" in runs

@pytest.mark.asyncio
async def test_get_and_update_settings(client):
    get_res = await client.get("/api/users/demo-user/settings")
    assert get_res.status_code == 200
    st = get_res.json()
    assert "preferredDifficulty" in st

    st["preferredDifficulty"] = "Advanced"
    put_res = await client.put("/api/users/demo-user/settings", json=st)
    assert put_res.status_code == 200
    assert put_res.json()["preferredDifficulty"] == "Advanced"
