import pytest
from app.agents.content_quality import ContentQualityAgent
from app.models.quality import QualityDecision, EvaluateCandidatesResponse

@pytest.mark.asyncio
async def test_agent4_genuine_backend_tutorial():
    """1. Genuine Backend Tutorial => ACCEPT"""
    agent = ContentQualityAgent()
    cand = {"candidateId": "C1", "title": "How REST APIs Connect Modern Applications", "description": "Designing clean, RESTful APIs.", "difficulty": "Intermediate"}
    res = await agent.evaluate_batch("user_1", [cand])
    eval_item = res.evaluations[0]
    
    assert eval_item.decision == QualityDecision.ACCEPT
    assert eval_item.hypeScore < 0.30
    assert eval_item.educationalValue >= 0.80

@pytest.mark.asyncio
async def test_agent4_ai_job_hype_trap():
    """2. AI Job Hype (Built-in Hype Trap) => REJECT"""
    agent = ContentQualityAgent()
    cand = {"candidateId": "C2", "title": "10 AI Tools That Will Get You A Job", "description": "Guaranteed $100K tech jobs overnight.", "difficulty": "Beginner"}
    res = await agent.evaluate_batch("user_1", [cand])
    eval_item = res.evaluations[0]
    
    # MUST BE REJECTED BY HYPE SHIELD
    assert eval_item.decision == QualityDecision.REJECT
    assert eval_item.hypeScore >= 0.80
    assert eval_item.clickbaitScore >= 0.80
    assert eval_item.misleadingClaimRisk >= 0.80

@pytest.mark.asyncio
async def test_agent4_developer_meme():
    """3. Developer Meme => High entertainment, NOT blanket rejected"""
    agent = ContentQualityAgent()
    cand = {"candidateId": "C3", "title": "When Your API Returns 500 in Production", "description": "Humorous developer meme about backend crashes.", "difficulty": "Intermediate"}
    res = await agent.evaluate_batch("user_1", [cand])
    eval_item = res.evaluations[0]
    
    assert eval_item.entertainmentValue >= 0.80
    assert eval_item.decision != QualityDecision.REJECT

@pytest.mark.asyncio
async def test_agent4_genuine_ai_tutorial():
    """4. Genuine AI Tutorial => ACCEPT"""
    agent = ContentQualityAgent()
    cand = {"candidateId": "C4", "title": "Build a Simple AI Agent with Python", "description": "Step-by-step practical guide to LLM tool calling.", "difficulty": "Intermediate"}
    res = await agent.evaluate_batch("user_1", [cand])
    eval_item = res.evaluations[0]
    
    assert eval_item.decision == QualityDecision.ACCEPT
    assert eval_item.practicalUsefulness >= 0.80

@pytest.mark.asyncio
async def test_agent4_unrealistic_career_claim():
    """5. Unrealistic Career Claim => REJECT"""
    agent = ContentQualityAgent()
    cand = {"candidateId": "C5", "title": "Learn Coding in 7 Days and Earn $10,000 a Month", "description": "Guaranteed secret trick to get rich.", "difficulty": "Beginner"}
    res = await agent.evaluate_batch("user_1", [cand])
    eval_item = res.evaluations[0]
    
    assert eval_item.decision == QualityDecision.REJECT
    assert eval_item.misleadingClaimRisk >= 0.85

@pytest.mark.asyncio
async def test_agent4_laptop_review():
    """6. Laptop Review => ACCEPT or PENALIZE"""
    agent = ContentQualityAgent()
    cand = {"candidateId": "C6", "title": "Best Laptop Specs for Software Developers", "description": "Comparing RAM, CPU, and battery life for coding.", "difficulty": "Beginner"}
    res = await agent.evaluate_batch("user_1", [cand])
    eval_item = res.evaluations[0]
    
    assert eval_item.decision in [QualityDecision.ACCEPT, QualityDecision.PENALIZE]

@pytest.mark.asyncio
async def test_agent4_promotional_content():
    """7. Promotional Content => PENALIZE or REJECT"""
    agent = ContentQualityAgent()
    cand = {"candidateId": "C7", "title": "Buy My $999 AI Masterclass Now", "description": "Limited spots remaining on this course.", "difficulty": "Beginner"}
    res = await agent.evaluate_batch("user_1", [cand])
    eval_item = res.evaluations[0]
    
    assert eval_item.promotionalScore >= 0.60
    assert eval_item.decision in [QualityDecision.PENALIZE, QualityDecision.REJECT]

@pytest.mark.asyncio
async def test_agent4_educational_tech_news():
    """8. Educational Tech News => ACCEPT"""
    agent = ContentQualityAgent()
    cand = {"candidateId": "C8", "title": "Python 3.12 Released: Substantive Technical Changes", "description": "Overview of new GIL performance improvements.", "difficulty": "Intermediate"}
    res = await agent.evaluate_batch("user_1", [cand])
    eval_item = res.evaluations[0]
    
    assert eval_item.decision == QualityDecision.ACCEPT

@pytest.mark.asyncio
async def test_agent4_evaluate_api_endpoint(client):
    """Integration Test: POST /api/recommendations/evaluate endpoint"""
    payload = {
        "userId": "student_001",
        "candidates": [
            {"candidateId": "T1", "title": "How REST APIs Connect Modern Applications", "description": "Clean REST API design."},
            {"candidateId": "T2", "title": "10 AI Tools That Will Get You A Job", "description": "Guaranteed $100K job."}
        ]
    }
    response = await client.post("/api/recommendations/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert data["success"] is True
    assert data["evaluatedCount"] == 2
    assert data["acceptedCount"] == 1
    assert data["rejectedCount"] == 1
