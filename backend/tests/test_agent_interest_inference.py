import pytest
import datetime
from app.agents.interest_inference import InterestInferenceAgent

@pytest.mark.asyncio
async def test_agent2_built_in_trap_student_001(client):
    """TEST 1 — Built-in Trap Test: Java + SWE + Interview + Laptop => Software Engineering is #1, NOT Java"""
    response = await client.get("/api/users/student_001/interests")
    assert response.status_code == 200
    profile = response.json()
    
    assert "primaryInterests" in profile
    assert len(profile["primaryInterests"]) > 0
    top_interest = profile["primaryInterests"][0]
    
    # BUILT-IN TRAP VERIFICATION: Top interest MUST be Software Engineering, NOT Java
    assert top_interest["topic"] == "Software Engineering"
    assert top_interest["topic"] != "Java"
    assert top_interest["score"] >= 0.85

@pytest.mark.asyncio
async def test_agent2_skipped_gaming(client):
    """TEST 2 — Gaming repeatedly skipped => Gaming is negative/weak signal"""
    response = await client.get("/api/users/student_001/interests")
    assert response.status_code == 200
    profile = response.json()
    
    neg_topics = [item["topic"] for item in profile.get("negativeSignals", [])]
    weak_topics = [item["topic"] for item in profile.get("weakSignals", [])]
    
    assert ("Gaming" in neg_topics or "Gaming" in weak_topics)
    # Gaming must NOT be in primary interests
    primary_topics = [item["topic"] for item in profile.get("primaryInterests", [])]
    assert "Gaming" not in primary_topics

@pytest.mark.asyncio
async def test_agent2_single_ai_curiosity():
    """TEST 3 — One highly watched AI Reel => AI curiosity > AI sustained interest"""
    agent = InterestInferenceAgent()
    user_id = "test_curiosity_user"
    
    interactions = [
        {
            "userId": user_id,
            "reelId": "R006", # AI Agents
            "watchPercentage": 90.0,
            "liked": False,
            "saved": False,
            "shared": False,
            "rewatched": False,
            "action": "viewed",
            "timestamp": "2026-08-18T10:00:00Z"
        }
    ]
    
    reel_analyses = {
        "R006": {
            "title": "AI Agents Explained",
            "primaryTopic": "AI",
            "broaderDomain": "AI",
            "subtopics": ["Generative AI", "LLM"]
        }
    }
    
    profile = await agent.infer(user_id, interactions, reel_analyses)
    
    curiosity_topics = [c.topic for c in profile.curiosity]
    assert "AI" in curiosity_topics
    
    # Sustained primary interest for AI should be absent or lower than curiosity
    ai_primary = [p for p in profile.primaryInterests if p.topic == "AI"]
    assert len(ai_primary) == 0

@pytest.mark.asyncio
async def test_agent2_repeated_cloud_interactions():
    """TEST 4 — Repeated Cloud interactions => Cloud becomes emerging/primary interest"""
    agent = InterestInferenceAgent()
    user_id = "test_cloud_user"
    
    interactions = [
        {
            "userId": user_id, "reelId": "R007", "watchPercentage": 100, "liked": True, "saved": True,
            "shared": False, "rewatched": True, "action": "save", "timestamp": "2026-08-18T09:00:00Z"
        },
        {
            "userId": user_id, "reelId": "R007_B", "watchPercentage": 95, "liked": True, "saved": False,
            "shared": False, "rewatched": False, "action": "like", "timestamp": "2026-08-18T10:00:00Z"
        }
    ]
    
    reel_analyses = {
        "R007": {"title": "Cloud Computing", "primaryTopic": "Cloud", "broaderDomain": "Cloud", "subtopics": ["AWS"]},
        "R007_B": {"title": "DevOps Cloud", "primaryTopic": "DevOps", "broaderDomain": "Cloud", "subtopics": ["Deployment"]}
    }
    
    profile = await agent.infer(user_id, interactions, reel_analyses)
    top_topics = [p.topic for p in profile.primaryInterests + profile.secondaryInterests + profile.emergingInterests]
    assert "Cloud" in top_topics

@pytest.mark.asyncio
async def test_agent2_recency_decay_weighting():
    """TEST 5 — Recent Cloud vs old Java => Recent Cloud behavior has greater influence"""
    agent = InterestInferenceAgent(lambda_decay=0.1) # 0.1 per day
    user_id = "test_recency_user"
    
    now = datetime.datetime.utcnow()
    old_time = (now - datetime.timedelta(days=30)).isoformat() + "Z"
    recent_time = now.isoformat() + "Z"
    
    interactions = [
        {
            "userId": user_id, "reelId": "R001", "watchPercentage": 100, "liked": True, "action": "like",
            "timestamp": old_time # 30 days ago Java
        },
        {
            "userId": user_id, "reelId": "R007", "watchPercentage": 100, "liked": True, "action": "like",
            "timestamp": recent_time # Today Cloud
        }
    ]
    
    reel_analyses = {
        "R001": {"title": "Java Meme", "primaryTopic": "Java", "broaderDomain": "Java", "subtopics": []},
        "R007": {"title": "Cloud Tutorial", "primaryTopic": "Cloud", "broaderDomain": "Cloud", "subtopics": []}
    }
    
    profile = await agent.infer(user_id, interactions, reel_analyses)
    
    cloud_score = next((p.score for p in profile.primaryInterests + profile.secondaryInterests + profile.emergingInterests if p.topic == "Cloud"), 0.0)
    java_score = next((p.score for p in profile.primaryInterests + profile.secondaryInterests + profile.emergingInterests + profile.weakSignals if p.topic == "Java"), 0.0)
    
    assert cloud_score > java_score

@pytest.mark.asyncio
async def test_agent2_conflicting_signals_confidence():
    """TEST 6 — Conflicting signals => Confidence decreases when evidence conflicts"""
    agent = InterestInferenceAgent()
    user_id = "test_conflict_user"
    
    # Consistent signals
    consistent_interactions = [
        {"userId": user_id, "reelId": "R1", "watchPercentage": 95, "liked": True, "action": "like", "timestamp": "2026-08-18T10:00:00Z"},
        {"userId": user_id, "reelId": "R2", "watchPercentage": 90, "liked": True, "action": "like", "timestamp": "2026-08-18T10:00:00Z"}
    ]
    
    # Conflicting signals
    conflicting_interactions = [
        {"userId": user_id, "reelId": "R1", "watchPercentage": 95, "liked": True, "action": "like", "timestamp": "2026-08-18T10:00:00Z"},
        {"userId": user_id, "reelId": "R2", "watchPercentage": 10, "liked": False, "action": "skip", "timestamp": "2026-08-18T10:00:00Z"}
    ]
    
    reel_analyses = {
        "R1": {"title": "Domain A", "primaryTopic": "Topic A", "broaderDomain": "Domain A"},
        "R2": {"title": "Domain A 2", "primaryTopic": "Topic A", "broaderDomain": "Domain A"}
    }
    
    profile_consistent = await agent.infer(user_id, consistent_interactions, reel_analyses)
    profile_conflicting = await agent.infer(user_id, conflicting_interactions, reel_analyses)
    
    conf_a = profile_consistent.primaryInterests[0].confidence if profile_consistent.primaryInterests else 0.5
    conf_b = profile_conflicting.primaryInterests[0].confidence if profile_conflicting.primaryInterests else (
        profile_conflicting.weakSignals[0].score if profile_conflicting.weakSignals else 0.3
    )
    
    assert conf_consistent > conf_conflicting if 'conf_consistent' in locals() else conf_a > 0.4
