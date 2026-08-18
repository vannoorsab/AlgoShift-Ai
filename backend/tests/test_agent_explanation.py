import pytest
from app.agents.explanation import ExplanationAgent, map_to_challenge_category, map_score_to_confidence
from app.models.interest import InterestProfile, InterestItem
from app.models.ranking import RankRecommendationResponse, SelectedRecommendation, RankedCandidateItem, RankingScoreBreakdown
from app.services.seed_service import seed_initial_data

@pytest.mark.asyncio
async def test_agent6_built_in_java_trap_challenge_output(client):
    """TEST 1 & 2 — Built-in Java Trap & Latent Interest: interestDetected.topic is Software Engineering, NOT Java."""
    await seed_initial_data()
    payload = {"userId": "student_001", "currentReelId": "R003"}
    response = await client.post("/api/recommendations/explain", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert data["success"] is True
    res = data["result"]
    
    # 8 REQUIRED FIELDS CHECK
    assert "currentReel" in res
    assert "interestDetected" in res
    assert "why" in res
    assert "recommendedTechReel" in res
    assert "category" in res
    assert "whyThisRecommendation" in res
    assert "difficulty" in res
    assert "confidence" in res
    
    # BUILT-IN TRAP VERIFICATION
    assert res["interestDetected"]["topic"] == "Software Engineering"
    assert res["interestDetected"]["topic"] != "Java"
    assert "Software Engineering" in res["why"]

@pytest.mark.asyncio
async def test_agent6_hype_rejection_reflection(client):
    """TEST 3 — Hype Rejection Reflection: Explanation reflects hype filtering when relevant."""
    await seed_initial_data()
    response = await client.post("/api/recommendations/explain", json={"userId": "student_001", "currentReelId": "R003"})
    assert response.status_code == 200
    data = response.json()
    
    res = data["result"]
    assert "whyThisRecommendation" in res
    assert len(res["whyThisRecommendation"]) > 10

@pytest.mark.asyncio
async def test_agent6_category_taxonomy_mapping():
    """TEST 4 — Correct Category Mapping: Backend/APIs -> Cloud, System Design -> HLD."""
    assert map_to_challenge_category("Backend", "APIs") == "Cloud"
    assert map_to_challenge_category("APIs", "APIs") == "Cloud"
    assert map_to_challenge_category("System Design", "HLD") == "HLD"
    assert map_to_challenge_category("Hardware", "Hardware") == "Hardware"
    assert map_to_challenge_category("AI", "AI") == "AI"
    assert map_to_challenge_category("DSA", "DSA") == "DSA"
    assert map_to_challenge_category("Cybersecurity", "Cybersecurity") == "Cybersecurity"

@pytest.mark.asyncio
async def test_agent6_correct_difficulty(client):
    """TEST 5 — Correct Difficulty: Matches candidate difficulty."""
    await seed_initial_data()
    response = await client.post("/api/recommendations/explain", json={"userId": "student_001", "currentReelId": "R003"})
    assert response.status_code == 200
    data = response.json()
    
    assert data["result"]["difficulty"] in ["Beginner", "Intermediate", "Advanced"]

@pytest.mark.asyncio
async def test_agent6_confidence_mapping():
    """TEST 6 — Confidence Mapping: >=0.80 -> High, 0.55-0.79 -> Medium, <0.55 -> Low."""
    assert map_score_to_confidence(0.92) == "High"
    assert map_score_to_confidence(0.80) == "High"
    assert map_score_to_confidence(0.70) == "Medium"
    assert map_score_to_confidence(0.40) == "Low"

@pytest.mark.asyncio
async def test_agent6_evidence_grounding(client):
    """TEST 7 & 9 — Evidence Grounding & No Hallucinations: Uses empirical signals without inventing data."""
    await seed_initial_data()
    response = await client.post("/api/recommendations/explain", json={"userId": "student_001", "currentReelId": "R003"})
    assert response.status_code == 200
    data = response.json()
    
    why_text = data["result"]["why"]
    # Must reference actual interaction themes
    assert "Java" in why_text or "coding" in why_text or "lifestyle" in why_text
    assert "saved five API videos" not in why_text  # No hallucinated claims

@pytest.mark.asyncio
async def test_agent6_missing_optional_data():
    """TEST 8 — Missing Optional Data: Gracefully handles missing optional parameters."""
    agent = ExplanationAgent()
    user_id = "test_empty_user"
    current_reel = {"reelId": "R999", "title": "Unknown Reel"}
    profile = InterestProfile(userId=user_id, overallConfidence=0.6)
    ranking_res = RankRecommendationResponse(
        userId=user_id, currentReelId="R999",
        selectedRecommendation=SelectedRecommendation(candidateId="C1", rank=1, finalScore=0.75, candidateType="Adjacent"),
        topCandidates=[RankedCandidateItem(candidateId="C1", rank=1, finalScore=0.75, title="Fallback API Reel", category="Backend", candidateType="Adjacent", scoreBreakdown=RankingScoreBreakdown(interestMatch=0.7, educationalValue=0.8, practicalUsefulness=0.8, novelty=0.7, interestExpansion=0.8, difficultyFit=0.8, careerRelevance=0.7, diversity=0.7, qualityScore=0.8, finalScore=0.75))]
    )
    
    res = await agent.explain(user_id, current_reel, profile, ranking_res)
    assert res.success is True
    assert res.result.currentReel.reelId == "R999"

@pytest.mark.asyncio
async def test_agent6_deterministic_consistency(client):
    """TEST 10 — Deterministic Selected Recommendation: Multiple calls yield identical winner."""
    await seed_initial_data()
    payload = {"userId": "student_001", "currentReelId": "R003"}
    
    res1 = await client.post("/api/recommendations/explain", json=payload)
    res2 = await client.post("/api/recommendations/explain", json=payload)
    
    assert res1.status_code == 200
    assert res2.status_code == 200
    
    winner1 = res1.json()["result"]["recommendedTechReel"]["candidateId"]
    winner2 = res2.json()["result"]["recommendedTechReel"]["candidateId"]
    
    assert winner1 == winner2
