import pytest
from app.agents.recommendation_ranking import RecommendationRankingAgent
from app.scoring.ranking_engine import RecommendationRankingEngine
from app.models.quality import QualityAssessment, QualityDecision
from app.models.interest import InterestProfile, InterestItem, FrontierItem
from app.services.seed_service import seed_initial_data

@pytest.mark.asyncio
async def test_agent5_high_similarity_low_educational():
    """TEST 1 — High similarity but low educational value: Useful candidate outranks it."""
    engine = RecommendationRankingEngine()
    user_id = "test_user_1"
    
    profile = InterestProfile(
        userId=user_id,
        primaryInterests=[InterestItem(topic="Java", score=0.9, confidence=0.9, evidence=[])],
        interestFrontier=[FrontierItem(topic="APIs", score=0.8)]
    )
    
    cand_low_edu = {"candidateId": "C1", "title": "Java Buzzwords", "topic": "Java", "category": "Backend", "candidateType": "Familiar", "difficulty": "Intermediate"}
    cand_high_edu = {"candidateId": "C2", "title": "REST APIs Explained", "topic": "APIs", "category": "Backend", "candidateType": "Adjacent", "difficulty": "Intermediate"}
    
    eval_low = QualityAssessment(candidateId="C1", educationalValue=0.20, practicalUsefulness=0.25, technicalDepth=0.20, careerRelevance=0.30, evidenceQuality=0.40, entertainmentValue=0.60, hypeScore=0.10, clickbaitScore=0.10, promotionalScore=0.0, misleadingClaimRisk=0.0, qualityScore=0.30, decision=QualityDecision.ACCEPT, reasons=[])
    eval_high = QualityAssessment(candidateId="C2", educationalValue=0.90, practicalUsefulness=0.92, technicalDepth=0.85, careerRelevance=0.80, evidenceQuality=0.85, entertainmentValue=0.55, hypeScore=0.05, clickbaitScore=0.05, promotionalScore=0.0, misleadingClaimRisk=0.0, qualityScore=0.88, decision=QualityDecision.ACCEPT, reasons=[])
    
    res = engine.rank_candidates(user_id, "R003", [cand_low_edu, cand_high_edu], [eval_low, eval_high], profile)
    assert res.selectedRecommendation.candidateId == "C2"

@pytest.mark.asyncio
async def test_agent5_high_hype_rejected_candidate():
    """TEST 2 — High hype candidate: Quality Gate filters REJECT decision so candidate cannot win."""
    engine = RecommendationRankingEngine()
    user_id = "test_user_2"
    
    profile = InterestProfile(
        userId=user_id,
        primaryInterests=[InterestItem(topic="AI", score=0.9, confidence=0.9, evidence=[])],
        interestFrontier=[]
    )
    
    cand_hype = {"candidateId": "C_HYPE", "title": "10 AI Tools That Will Get You A Job", "topic": "AI", "category": "AI", "candidateType": "Familiar", "difficulty": "Intermediate"}
    cand_good = {"candidateId": "C_GOOD", "title": "Build a Simple AI Agent with Python", "topic": "AI", "category": "AI", "candidateType": "Familiar", "difficulty": "Intermediate"}
    
    eval_hype = QualityAssessment(candidateId="C_HYPE", educationalValue=0.30, practicalUsefulness=0.28, technicalDepth=0.25, careerRelevance=0.40, evidenceQuality=0.30, entertainmentValue=0.60, hypeScore=0.95, clickbaitScore=0.88, promotionalScore=0.0, misleadingClaimRisk=0.90, qualityScore=0.0, decision=QualityDecision.REJECT, reasons=["High hype"])
    eval_good = QualityAssessment(candidateId="C_GOOD", educationalValue=0.88, practicalUsefulness=0.90, technicalDepth=0.80, careerRelevance=0.75, evidenceQuality=0.85, entertainmentValue=0.55, hypeScore=0.10, clickbaitScore=0.05, promotionalScore=0.0, misleadingClaimRisk=0.0, qualityScore=0.84, decision=QualityDecision.ACCEPT, reasons=[])
    
    res = engine.rank_candidates(user_id, "R003", [cand_hype, cand_good], [eval_hype, eval_good], profile)
    assert res.selectedRecommendation.candidateId == "C_GOOD"
    assert "C_HYPE" not in [c.candidateId for c in res.topCandidates]

@pytest.mark.asyncio
async def test_agent5_repeated_java_recommendations():
    """TEST 3 — Repeated Java recommendations: Diversity/duplicate penalties reduce Java candidate score."""
    engine = RecommendationRankingEngine()
    user_id = "test_user_3"
    
    profile = InterestProfile(
        userId=user_id,
        primaryInterests=[InterestItem(topic="Software Engineering", score=0.9, confidence=0.9, evidence=[])],
        interestFrontier=[FrontierItem(topic="APIs", score=0.8)]
    )
    
    cand_java = {"candidateId": "C_JAVA", "title": "Java Basics", "topic": "Java", "category": "Backend", "candidateType": "Familiar", "difficulty": "Intermediate"}
    cand_api = {"candidateId": "C_API", "title": "REST APIs Explained", "topic": "APIs", "category": "Backend", "candidateType": "Adjacent", "difficulty": "Intermediate"}
    
    eval_gen = QualityAssessment(candidateId="C", educationalValue=0.85, practicalUsefulness=0.85, technicalDepth=0.75, careerRelevance=0.70, evidenceQuality=0.80, entertainmentValue=0.50, hypeScore=0.05, clickbaitScore=0.05, promotionalScore=0.0, misleadingClaimRisk=0.0, qualityScore=0.82, decision=QualityDecision.ACCEPT, reasons=[])
    
    # 2 Java items already recently consumed
    res = engine.rank_candidates(user_id, "R003", [cand_java, cand_api], [eval_gen, eval_gen], profile, recently_consumed_topics=["Java", "Java"])
    assert res.selectedRecommendation.candidateId == "C_API"

@pytest.mark.asyncio
async def test_agent5_strong_adjacent_candidate():
    """TEST 4 — Strong adjacent candidate: Adjacent candidate beats repetitive familiar candidate."""
    engine = RecommendationRankingEngine()
    user_id = "test_user_4"
    
    profile = InterestProfile(
        userId=user_id,
        primaryInterests=[InterestItem(topic="Software Engineering", score=0.9, confidence=0.9, evidence=[])],
        interestFrontier=[FrontierItem(topic="Backend", score=0.85), FrontierItem(topic="APIs", score=0.82)]
    )
    
    cand_fam = {"candidateId": "C_FAM", "title": "Java Syntax Tricks", "topic": "Java", "category": "Backend", "candidateType": "Familiar", "difficulty": "Intermediate"}
    cand_adj = {"candidateId": "C_ADJ", "title": "Database Indexing & Query Optimization", "topic": "Databases", "category": "Databases", "candidateType": "Adjacent", "difficulty": "Intermediate"}
    
    eval_gen = QualityAssessment(candidateId="C", educationalValue=0.88, practicalUsefulness=0.90, technicalDepth=0.80, careerRelevance=0.75, evidenceQuality=0.80, entertainmentValue=0.55, hypeScore=0.05, clickbaitScore=0.05, promotionalScore=0.0, misleadingClaimRisk=0.0, qualityScore=0.84, decision=QualityDecision.ACCEPT, reasons=[])
    
    res = engine.rank_candidates(user_id, "R003", [cand_fam, cand_adj], [eval_gen, eval_gen], profile)
    assert res.selectedRecommendation.candidateId == "C_ADJ"

@pytest.mark.asyncio
async def test_agent5_unrelated_novel_content():
    """TEST 5 — Unrelated novel content: Novelty alone cannot make unrelated candidate win."""
    engine = RecommendationRankingEngine()
    user_id = "test_user_5"
    
    profile = InterestProfile(
        userId=user_id,
        primaryInterests=[InterestItem(topic="Software Engineering", score=0.9, confidence=0.9, evidence=[])],
        interestFrontier=[FrontierItem(topic="Backend", score=0.8)]
    )
    
    cand_related = {"candidateId": "C_REL", "title": "REST APIs Design", "topic": "Backend", "category": "Backend", "candidateType": "Adjacent", "novelty": 0.70, "difficulty": "Intermediate"}
    cand_unrelated = {"candidateId": "C_UNREL", "title": "Quantum Mechanics Basics", "topic": "Physics", "category": "Other", "candidateType": "Exploratory", "novelty": 0.99, "difficulty": "Intermediate"}
    
    eval_gen = QualityAssessment(candidateId="C", educationalValue=0.85, practicalUsefulness=0.80, technicalDepth=0.75, careerRelevance=0.70, evidenceQuality=0.80, entertainmentValue=0.50, hypeScore=0.05, clickbaitScore=0.05, promotionalScore=0.0, misleadingClaimRisk=0.0, qualityScore=0.80, decision=QualityDecision.ACCEPT, reasons=[])
    
    res = engine.rank_candidates(user_id, "R003", [cand_related, cand_unrelated], [eval_gen, eval_gen], profile)
    assert res.selectedRecommendation.candidateId == "C_REL"

@pytest.mark.asyncio
async def test_agent5_difficulty_mismatch():
    """TEST 6 — Difficulty mismatch: Strong penalty for inappropriate difficulty."""
    engine = RecommendationRankingEngine()
    user_id = "test_user_6"
    
    profile = InterestProfile(
        userId=user_id,
        primaryInterests=[InterestItem(topic="Software Engineering", score=0.9, confidence=0.9, evidence=[])],
        interestFrontier=[]
    )
    
    cand_inter = {"candidateId": "C_INT", "title": "Intermediate APIs", "topic": "Backend", "category": "Backend", "candidateType": "Adjacent", "difficulty": "Intermediate"}
    cand_adv = {"candidateId": "C_ADV", "title": "Advanced Distributed Systems", "topic": "Backend", "category": "Backend", "candidateType": "Adjacent", "difficulty": "Advanced"}
    
    eval_gen = QualityAssessment(candidateId="C", educationalValue=0.85, practicalUsefulness=0.85, technicalDepth=0.85, careerRelevance=0.75, evidenceQuality=0.80, entertainmentValue=0.50, hypeScore=0.05, clickbaitScore=0.05, promotionalScore=0.0, misleadingClaimRisk=0.0, qualityScore=0.82, decision=QualityDecision.ACCEPT, reasons=[])
    
    res = engine.rank_candidates(user_id, "R003", [cand_inter, cand_adv], [eval_gen, eval_gen], profile, user_difficulty="Beginner")
    assert res.selectedRecommendation.candidateId == "C_INT"

@pytest.mark.asyncio
async def test_agent5_previously_rejected_content():
    """TEST 7 — Previously rejected content: Rejection penalty prevents winning."""
    engine = RecommendationRankingEngine()
    user_id = "test_user_7"
    
    profile = InterestProfile(
        userId=user_id,
        primaryInterests=[InterestItem(topic="Software Engineering", score=0.9, confidence=0.9, evidence=[])],
        interestFrontier=[]
    )
    
    cand_rej = {"candidateId": "C_REJ", "title": "Java Backend Microservices", "topic": "Java", "category": "Backend", "candidateType": "Familiar", "difficulty": "Intermediate"}
    cand_good = {"candidateId": "C_GOOD", "title": "Database Indexing", "topic": "Databases", "category": "Databases", "candidateType": "Adjacent", "difficulty": "Intermediate"}
    
    eval_gen = QualityAssessment(candidateId="C", educationalValue=0.88, practicalUsefulness=0.88, technicalDepth=0.80, careerRelevance=0.75, evidenceQuality=0.80, entertainmentValue=0.50, hypeScore=0.05, clickbaitScore=0.05, promotionalScore=0.0, misleadingClaimRisk=0.0, qualityScore=0.85, decision=QualityDecision.ACCEPT, reasons=[])
    
    res = engine.rank_candidates(user_id, "R003", [cand_rej, cand_good], [eval_gen, eval_gen], profile, rejected_candidate_ids=["C_REJ"])
    assert res.selectedRecommendation.candidateId == "C_GOOD"

@pytest.mark.asyncio
async def test_agent5_built_in_challenge_trap(client):
    """TEST 8 — Built-in challenge trap: Useful adjacent recommendation wins over generic Java/hype content."""
    await seed_initial_data()
    
    custom_candidates = [
        {"candidateId": "C1", "title": "Generic Java Tutorial", "topic": "Java", "category": "Backend", "candidateType": "Familiar", "difficulty": "Intermediate"},
        {"candidateId": "C2", "title": "How APIs Connect Modern Applications", "topic": "APIs", "category": "Backend", "candidateType": "Adjacent", "difficulty": "Intermediate"},
        {"candidateId": "C3", "title": "Cloud Architecture Basics", "topic": "Cloud", "category": "Cloud", "candidateType": "Exploratory", "difficulty": "Intermediate"},
        {"candidateId": "C4", "title": "10 AI Tools That Will Get You A Job", "topic": "AI", "category": "AI", "candidateType": "Familiar", "difficulty": "Intermediate"},
        {"candidateId": "C5", "title": "Java Developer Meme", "topic": "Java", "category": "Backend", "candidateType": "Familiar", "difficulty": "Intermediate"},
        {"candidateId": "C6", "title": "Database Indexing Explained", "topic": "Databases", "category": "Databases", "candidateType": "Adjacent", "difficulty": "Intermediate"}
    ]
    
    payload = {
        "userId": "student_001",
        "currentReelId": "R003",
        "candidates": custom_candidates
    }
    
    response = await client.post("/api/recommendations/rank", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    winner_id = data["selectedRecommendation"]["candidateId"]
    top_ids = [c["candidateId"] for c in data["topCandidates"]]
    
    # 1. Hype item C4 MUST NOT win
    assert winner_id != "C4"
    assert "C4" not in top_ids
    
    # 2. Useful adjacent candidate (C2 or C6) MUST win
    assert winner_id in ["C2", "C6"]
    assert len(data["topCandidates"]) == 3
