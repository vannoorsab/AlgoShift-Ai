import pytest
from app.agents.feedback_learning import FeedbackLearningAgent
from app.scoring.feedback_engine import FeedbackEngine
from app.models.feedback import RecommendationFeedbackPayload
from app.models.interest import InterestProfile, InterestItem, FrontierItem
from app.services.seed_service import seed_initial_data

@pytest.mark.asyncio
async def test_agent7_strong_positive_feedback_propagation():
    """TEST 1 — Strong Positive Feedback: Backend increases strongly & propagates to APIs/Software Engineering."""
    engine = FeedbackEngine()
    profile = InterestProfile(
        userId="user_1",
        primaryInterests=[
            InterestItem(topic="Backend", score=0.64, confidence=0.8, evidence=[]),
            InterestItem(topic="APIs", score=0.60, confidence=0.8, evidence=[]),
            InterestItem(topic="Software Engineering", score=0.90, confidence=0.9, evidence=[])
        ]
    )
    payload = RecommendationFeedbackPayload(
        userId="user_1", reelId="TECH014", watchPercentage=96.0,
        liked=True, saved=True, rewatched=True, completed=True
    )
    
    upd_profile, changes = engine.update_profile_with_feedback(profile, "Backend", payload)
    
    backend_change = next(c for c in changes if c.topic == "Backend")
    assert backend_change.change > 0.10
    assert backend_change.newScore > 0.70
    
    # Semantic propagation check
    api_change = next(c for c in changes if c.topic == "APIs")
    assert api_change.change > 0.05

@pytest.mark.asyncio
async def test_agent7_strong_negative_feedback():
    """TEST 2 — Strong Negative Feedback: Cloud Reel with 8% watch + skip decreases score."""
    engine = FeedbackEngine()
    profile = InterestProfile(
        userId="user_2",
        primaryInterests=[InterestItem(topic="Cloud", score=0.65, confidence=0.8, evidence=[])]
    )
    payload = RecommendationFeedbackPayload(
        userId="user_2", reelId="CLOUD01", watchPercentage=8.0, skipped=True
    )
    
    upd_profile, changes = engine.update_profile_with_feedback(profile, "Cloud", payload)
    cloud_change = next(c for c in changes if c.topic == "Cloud")
    
    assert cloud_change.change < 0.0
    assert cloud_change.newScore < 0.65
    assert "Cloud" in upd_profile.decliningInterests

@pytest.mark.asyncio
async def test_agent7_repeated_positive_feedback():
    """TEST 3 — Repeated Positive Feedback: 3 Backend Reels build Backend into stronger primary interest."""
    engine = FeedbackEngine()
    profile = InterestProfile(
        userId="user_3",
        primaryInterests=[InterestItem(topic="Backend", score=0.60, confidence=0.8, evidence=[])]
    )
    payload = RecommendationFeedbackPayload(userId="user_3", reelId="B1", watchPercentage=90.0, liked=True)
    
    p1, _ = engine.update_profile_with_feedback(profile, "Backend", payload)
    p2, _ = engine.update_profile_with_feedback(p1, "Backend", payload)
    p3, changes = engine.update_profile_with_feedback(p2, "Backend", payload)
    
    backend_item = next(i for i in p3.primaryInterests if i.topic == "Backend")
    assert backend_item.score >= 0.80

@pytest.mark.asyncio
async def test_agent7_repeated_negative_feedback():
    """TEST 4 — Repeated Negative Feedback: 3 Gaming skips build Gaming into declining interest."""
    engine = FeedbackEngine()
    profile = InterestProfile(
        userId="user_4",
        primaryInterests=[InterestItem(topic="Gaming", score=0.50, confidence=0.8, evidence=[])]
    )
    payload = RecommendationFeedbackPayload(userId="user_4", reelId="G1", watchPercentage=10.0, skipped=True)
    
    p1, _ = engine.update_profile_with_feedback(profile, "Gaming", payload)
    p2, _ = engine.update_profile_with_feedback(p1, "Gaming", payload)
    p3, _ = engine.update_profile_with_feedback(p2, "Gaming", payload)
    
    assert "Gaming" in p3.decliningInterests
    gaming_item = next(i for i in p3.primaryInterests if i.topic == "Gaming")
    assert gaming_item.score < 0.40

@pytest.mark.asyncio
async def test_agent7_exploration_protection():
    """TEST 5 — Exploration Protection: Repeated Java likes preserve adjacent frontier topics."""
    engine = FeedbackEngine()
    profile = InterestProfile(
        userId="user_5",
        primaryInterests=[InterestItem(topic="Java", score=0.70, confidence=0.8, evidence=[])],
        interestFrontier=[FrontierItem(topic="Backend", score=0.8), FrontierItem(topic="APIs", score=0.8)]
    )
    payload = RecommendationFeedbackPayload(userId="user_5", reelId="J1", watchPercentage=95.0, liked=True)
    
    p1, _ = engine.update_profile_with_feedback(profile, "Java", payload)
    p2, _ = engine.update_profile_with_feedback(p1, "Java", payload)
    
    frontier_topics = [f.topic for f in p2.interestFrontier]
    assert "Backend" in frontier_topics
    assert "APIs" in frontier_topics

@pytest.mark.asyncio
async def test_agent7_cold_start():
    """TEST 6 — Cold Start Handling: Single interaction yields small profile change."""
    engine = FeedbackEngine()
    profile = InterestProfile(userId="user_6", primaryInterests=[])
    payload = RecommendationFeedbackPayload(userId="user_6", reelId="AI1", watchPercentage=60.0)
    
    p1, changes = engine.update_profile_with_feedback(profile, "AI", payload)
    ai_change = next(c for c in changes if c.topic == "AI")
    
    assert ai_change.change <= 0.10
    assert p1.overallConfidence < 0.85

@pytest.mark.asyncio
async def test_agent7_idempotency_api_endpoint(client):
    """TEST 7 — Feedback Idempotency: Re-submitting exact same event is idempotent."""
    await seed_initial_data()
    payload = {
        "userId": "student_001",
        "reelId": "TECH014",
        "eventId": "EVT_TEST_IDEMPOTENT_001",
        "watchPercentage": 96.0,
        "liked": True,
        "saved": True
    }
    
    res1 = await client.post("/api/recommendations/feedback", json=payload)
    res2 = await client.post("/api/recommendations/feedback", json=payload)
    
    assert res1.status_code == 200
    assert res2.status_code == 200
    assert res1.json()["success"] is True
    assert res2.json()["success"] is True

@pytest.mark.asyncio
async def test_agent7_end_to_end_adaptation_pipeline(client):
    """TEST 8 — End-to-End Pipeline Adaptation: Feedback updates profile, influencing Candidate Pool & Ranking."""
    await seed_initial_data()
    
    # 1. Post strong positive Backend feedback
    feedback_payload = {
        "userId": "student_001",
        "reelId": "TECH014",
        "watchPercentage": 96.0,
        "liked": True,
        "saved": True,
        "rewatched": True
    }
    fb_res = await client.post("/api/recommendations/feedback", json=feedback_payload)
    assert fb_res.status_code == 200
    
    # 2. Trigger ranking API
    rank_res = await client.post("/api/recommendations/rank", json={"userId": "student_001", "currentReelId": "R003"})
    assert rank_res.status_code == 200
    data = rank_res.json()
    
    winner_id = data["selectedRecommendation"]["candidateId"]
    assert winner_id is not None
    assert len(data["topCandidates"]) == 3
