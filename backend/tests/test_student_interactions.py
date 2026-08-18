import pytest
from app.repositories.interaction_repository import InteractionRepository

@pytest.mark.asyncio
async def test_student_001_interactions_exist():
    repo = InteractionRepository()
    interactions = await repo.get_by_user("student_001", limit=100)
    
    assert len(interactions) == 8
    
    reel_map = {item["reelId"]: item for item in interactions}
    
    # R001 — Java Developer Meme
    r1 = reel_map["R001"]
    assert r1["watchPercentage"] == 95
    assert r1["liked"] is True
    assert r1["saved"] is False
    assert r1["rewatched"] is True
    assert r1["action"] == "like"
    
    # R002 — Software Engineer Lifestyle
    r2 = reel_map["R002"]
    assert r2["watchPercentage"] == 100
    assert r2["liked"] is True
    assert r2["saved"] is True
    assert r2["action"] == "save"
    
    # R003 — Coding Interview Joke
    r3 = reel_map["R003"]
    assert r3["watchPercentage"] == 92
    assert r3["rewatched"] is True
    assert r3["action"] == "replay"
    
    # R004 — Laptop Comparison
    r4 = reel_map["R004"]
    assert r4["watchPercentage"] == 88
    assert r4["liked"] is True
    assert r4["action"] == "like"
    
    # R005 — Gaming Highlights
    r5 = reel_map["R005"]
    assert r5["watchPercentage"] == 12
    assert r5["action"] == "skip"
    
    # R006 — AI Agents Explained
    r6 = reel_map["R006"]
    assert r6["watchPercentage"] == 42
    assert r6["action"] == "viewed"
    
    # R007 — Cloud Computing Explained
    r7 = reel_map["R007"]
    assert r7["watchPercentage"] == 25
    assert r7["action"] == "skip"
    
    # R008 — Technology News
    r8 = reel_map["R008"]
    assert r8["watchPercentage"] == 65
    assert r8["action"] == "viewed"
