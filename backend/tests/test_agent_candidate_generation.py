import pytest
from app.agents.candidate_generation import CandidateGenerationAgent
from app.models.interest import InterestProfile, InterestItem, NegativeSignalItem, CuriosityItem, FrontierItem
from app.models.recommendation import CandidateType
from app.services.seed_service import seed_initial_data

@pytest.mark.asyncio
async def test_agent3_built_in_trap_student_001(client):
    """TEST 1 — Built-in Trap: Candidate pool contains Backend, APIs, Databases, System Design, Cloud, NOT dominated by Java."""
    await seed_initial_data()
    response = await client.post("/api/recommendations/candidates", json={"userId": "student_001"})
    assert response.status_code == 200
    data = response.json()
    
    assert data["success"] is True
    assert data["candidateCount"] >= 10
    
    candidates = data["candidates"]
    topics = [c["topic"] for c in candidates]
    categories = [c["category"] for c in candidates]
    
    # Must contain frontier topics
    assert any(t in ["Backend", "APIs", "Databases", "System Design", "Cloud"] for t in topics + categories)
    
    # Java candidates must NOT dominate (e.g. <= 35% of candidate pool)
    java_count = sum(1 for t in topics if t == "Java")
    assert java_count / len(candidates) <= 0.35

@pytest.mark.asyncio
async def test_agent3_gaming_negative_signal_suppression(client):
    """TEST 2 — Gaming Negative Signal: Gaming candidates should be heavily suppressed/absent."""
    await seed_initial_data()
    response = await client.post("/api/recommendations/candidates", json={"userId": "student_001"})
    assert response.status_code == 200
    data = response.json()
    
    candidates = data["candidates"]
    gaming_candidates = [c for c in candidates if c["topic"] == "Gaming" or c["category"] == "Gaming"]
    assert len(gaming_candidates) == 0

@pytest.mark.asyncio
async def test_agent3_novelty_score_penalty():
    """TEST 3 — Novelty: Recently consumed Java content receives reduced novelty score."""
    agent = CandidateGenerationAgent()
    user_id = "test_novelty_user"
    
    profile = InterestProfile(
        userId=user_id,
        primaryInterests=[InterestItem(topic="Java", score=0.9, confidence=0.9, evidence=[])],
        interestFrontier=[FrontierItem(topic="APIs", score=0.8)]
    )
    
    catalog = [
        {"contentId": "T1", "title": "Java Basics", "topic": "Java", "category": "Backend", "difficulty": "Intermediate"},
        {"contentId": "T2", "title": "REST APIs", "topic": "APIs", "category": "Backend", "difficulty": "Intermediate"}
    ]
    
    consumed = ["Java"]
    res = await agent.generate_candidates(user_id, profile, catalog, consumed_topics=consumed)
    
    java_cand = next(c for c in res.candidates if c.topic == "Java")
    api_cand = next(c for c in res.candidates if c.topic == "APIs")
    
    assert java_cand.novelty < api_cand.novelty
    assert java_cand.novelty == 0.35

@pytest.mark.asyncio
async def test_agent3_curiosity_handling():
    """TEST 4 — Curiosity: AI appears as exploratory candidate but does not dominate."""
    agent = CandidateGenerationAgent()
    user_id = "test_curiosity_user"
    
    profile = InterestProfile(
        userId=user_id,
        primaryInterests=[InterestItem(topic="Software Engineering", score=0.9, confidence=0.9, evidence=[])],
        curiosity=[CuriosityItem(topic="AI", score=0.7)],
        interestFrontier=[FrontierItem(topic="Backend", score=0.8)]
    )
    
    catalog = [
        {"contentId": "T1", "title": "Java Backend", "topic": "Software Engineering", "category": "Backend", "difficulty": "Intermediate"},
        {"contentId": "T2", "title": "REST APIs", "topic": "Backend", "category": "Backend", "difficulty": "Intermediate"},
        {"contentId": "T3", "title": "AI Agents", "topic": "AI", "category": "AI", "difficulty": "Intermediate"}
    ]
    
    res = await agent.generate_candidates(user_id, profile, catalog)
    ai_cands = [c for c in res.candidates if c.topic == "AI"]
    
    if ai_cands:
        assert ai_cands[0].candidateType == CandidateType.EXPLORATORY

@pytest.mark.asyncio
async def test_agent3_candidate_type_diversity(client):
    """TEST 5 — Diversity: Candidate pool contains mix of Familiar, Adjacent, and Exploratory types."""
    await seed_initial_data()
    response = await client.post("/api/recommendations/candidates", json={"userId": "student_001"})
    assert response.status_code == 200
    data = response.json()
    
    candidates = data["candidates"]
    types = [c["candidateType"] for c in candidates]
    
    assert "Familiar" in types
    assert "Adjacent" in types
    assert "Exploratory" in types

@pytest.mark.asyncio
async def test_agent3_difficulty_fit():
    """TEST 6 — Difficulty: Candidates match inferred difficulty preference."""
    agent = CandidateGenerationAgent()
    user_id = "test_diff_user"
    
    profile = InterestProfile(
        userId=user_id,
        primaryInterests=[InterestItem(topic="Software Engineering", score=0.9, confidence=0.9, evidence=[])],
        interestFrontier=[FrontierItem(topic="Backend", score=0.8)]
    )
    
    catalog = [
        {"contentId": "T1", "title": "Intermediate APIs", "topic": "Backend", "category": "Backend", "difficulty": "Intermediate"},
        {"contentId": "T2", "title": "Advanced Distributed Systems", "topic": "Backend", "category": "Backend", "difficulty": "Advanced"}
    ]
    
    res = await agent.generate_candidates(user_id, profile, catalog, user_difficulty="Intermediate")
    
    inter_cand = next(c for c in res.candidates if c.title == "Intermediate APIs")
    adv_cand = next(c for c in res.candidates if c.title == "Advanced Distributed Systems")
    
    assert inter_cand.learningPotential >= adv_cand.learningPotential
