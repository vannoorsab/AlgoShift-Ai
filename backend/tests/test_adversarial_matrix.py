import pytest
from app.agents.interest_inference import InterestInferenceAgent
from app.agents.content_quality import ContentQualityAgent
from app.agents.recommendation_ranking import RecommendationRankingAgent
from app.agents.explanation import ExplanationAgent, TaxonomyMapper
from app.models.quality import QualityDecision, QualityAssessment

@pytest.fixture
def agent2():
    return InterestInferenceAgent()

@pytest.fixture
def agent4():
    return ContentQualityAgent()

@pytest.fixture
def agent5():
    return RecommendationRankingAgent()

@pytest.fixture
def agent6():
    return ExplanationAgent()


# ============================================================================
# TEST A: Java meme + SWE lifestyle + Coding interview joke + Laptop comparison
# Expected: Software Engineering (NOT Java-only)
# ============================================================================
@pytest.mark.asyncio
async def test_adversarial_test_a_software_engineering_inference(agent2):
    interactions = [
        {"reelId": "R001", "watchPercentage": 95.0, "liked": True, "saved": False, "action": "like"},
        {"reelId": "R002", "watchPercentage": 88.0, "liked": False, "saved": True, "action": "save"},
        {"reelId": "R003", "watchPercentage": 100.0, "liked": True, "saved": True, "action": "replay"},
        {"reelId": "R004", "watchPercentage": 82.0, "liked": True, "saved": False, "action": "like"},
    ]
    reel_analyses = {
        "R001": {"title": "Java Developers at 2 AM", "primaryTopic": "Java", "broaderDomain": "Software Engineering"},
        "R002": {"title": "Day in Life of SWE", "primaryTopic": "Software Engineering", "broaderDomain": "Software Engineering"},
        "R003": {"title": "Coding Interview Joke", "primaryTopic": "Coding Interviews", "broaderDomain": "Software Engineering"},
        "R004": {"title": "MacBook vs XPS for Coding", "primaryTopic": "Developer Hardware", "broaderDomain": "Software Engineering"},
    }

    profile = await agent2.infer("student_001", interactions, reel_analyses)
    assert len(profile.primaryInterests) > 0
    top_domain = profile.primaryInterests[0].topic
    assert top_domain == "Software Engineering"
    assert top_domain != "Java"


# ============================================================================
# TEST B: Python tutorial + Python meme + Python syntax joke
# Expected: Software Engineering / Programming broader interest
# ============================================================================
@pytest.mark.asyncio
async def test_adversarial_test_b_python_broader_domain_inference(agent2):
    interactions = [
        {"reelId": "PY001", "watchPercentage": 90.0, "liked": True, "saved": False},
        {"reelId": "PY002", "watchPercentage": 85.0, "liked": True, "saved": True},
        {"reelId": "PY003", "watchPercentage": 92.0, "liked": True, "saved": False},
    ]
    reel_analyses = {
        "PY001": {"title": "Python Basics Tutorial", "primaryTopic": "Python", "broaderDomain": "Programming"},
        "PY002": {"title": "Python List Comprehension Meme", "primaryTopic": "Python", "broaderDomain": "Programming"},
        "PY003": {"title": "Python vs C++ Speed Joke", "primaryTopic": "Python", "broaderDomain": "Programming"},
    }

    profile = await agent2.infer("student_python", interactions, reel_analyses)
    assert len(profile.primaryInterests) > 0
    top_topic = profile.primaryInterests[0].topic
    assert top_topic in ["Programming", "Software Engineering", "Python"]


# ============================================================================
# TEST C: AI Hype ("10 AI Tools That Will Get You A Job")
# Expected: Quality layer REJECT / PENALIZE (Must not win on hype alone)
# ============================================================================
@pytest.mark.asyncio
async def test_adversarial_test_c_ai_hype_rejection(agent4):
    hype_candidate = {
        "candidateId": "CAND_HYPE_01",
        "title": "10 Secret AI Tools That Will Get You A Job In 30 Days",
        "caption": "10 Secret AI Tools That Will Get You A Job In 30 Days",
        "topic": "AI",
        "educationalValue": 0.20,
        "hypeScore": 0.95,
        "clickbaitScore": 0.90,
        "promotionalScore": 0.85,
        "misleadingClaimRisk": 0.88,
    }

    eval_res = await agent4.evaluate_batch("student_001", [hype_candidate])
    eval_result = eval_res.evaluations[0]
    assert eval_result.decision in [QualityDecision.REJECT, QualityDecision.PENALIZE]


# ============================================================================
# TEST D: Cybersecurity content (CTF, SOC, Threat Detection)
# Expected: Category mapped to Cybersecurity
# ============================================================================
def test_adversarial_test_d_cybersecurity_taxonomy_mapping():
    cat1 = TaxonomyMapper.map_category("Cybersecurity", "CTF")
    cat2 = TaxonomyMapper.map_category("Security", "Threat Detection")
    cat3 = TaxonomyMapper.map_category("Networking", "SOC Analyst")

    assert cat1 == "Cybersecurity"
    assert cat2 == "Cybersecurity"
    assert cat3 == "Cybersecurity"


# ============================================================================
# TEST E: Cloud content (Docker, Kubernetes, Cloud Architecture)
# Expected: Category mapped to Cloud
# ============================================================================
def test_adversarial_test_e_cloud_taxonomy_mapping():
    cat1 = TaxonomyMapper.map_category("DevOps", "Docker Containerization")
    cat2 = TaxonomyMapper.map_category("Cloud", "AWS Cloud Architecture")

    assert cat1 == "Cloud"
    assert cat2 == "Cloud"


# ============================================================================
# TEST F: Mixed entertainment + one technical Reel
# Expected: Single interaction does NOT immediately promote topic to PrimaryInterest
# ============================================================================
@pytest.mark.asyncio
async def test_adversarial_test_f_isolated_interaction_threshold(agent2):
    interactions = [
        {"reelId": "ENT001", "watchPercentage": 90.0, "liked": False, "action": "watch"},
        {"reelId": "ENT002", "watchPercentage": 85.0, "liked": False, "action": "watch"},
        {"reelId": "SINGLE_TECH", "watchPercentage": 95.0, "liked": True, "action": "like"},
    ]
    reel_analyses = {
        "ENT001": {"title": "Gaming Funny Moments", "primaryTopic": "Gaming", "broaderDomain": "Gaming"},
        "ENT002": {"title": "Tech Meme Compilation", "primaryTopic": "Humor", "broaderDomain": "Humor"},
        "SINGLE_TECH": {"title": "Advanced Quantum Computing", "primaryTopic": "Quantum Computing", "broaderDomain": "Quantum Computing"},
    }

    profile = await agent2.infer("student_mixed", interactions, reel_analyses)
    primary_topics = [p.topic for p in profile.primaryInterests]
    assert "Quantum Computing" not in primary_topics


# ============================================================================
# TEST G: Multiple unrelated technology topics
# Expected: Diversified interest profile
# ============================================================================
@pytest.mark.asyncio
async def test_adversarial_test_g_diversified_interest_profile(agent2):
    interactions = [
        {"reelId": "T1", "watchPercentage": 90.0, "liked": True, "saved": True},
        {"reelId": "T2", "watchPercentage": 92.0, "liked": True, "saved": True},
        {"reelId": "C1", "watchPercentage": 88.0, "liked": True, "saved": False},
        {"reelId": "C2", "watchPercentage": 85.0, "liked": True, "saved": False},
    ]
    reel_analyses = {
        "T1": {"title": "DSA Binary Trees", "primaryTopic": "DSA", "broaderDomain": "DSA"},
        "T2": {"title": "DSA Graph Algorithms", "primaryTopic": "DSA", "broaderDomain": "DSA"},
        "C1": {"title": "Docker Setup", "primaryTopic": "DevOps", "broaderDomain": "DevOps"},
        "C2": {"title": "Kubernetes Pods", "primaryTopic": "DevOps", "broaderDomain": "DevOps"},
    }

    profile = await agent2.infer("student_diversified", interactions, reel_analyses)
    topics = [p.topic for p in profile.primaryInterests + profile.secondaryInterests + profile.emergingInterests]
    assert len(topics) >= 2


# ============================================================================
# TEST H: Repeated Java + Backend + REST APIs
# Expected: Recommends Backend/APIs rather than repeating generic Java
# ============================================================================
@pytest.mark.asyncio
async def test_adversarial_test_h_avoid_blind_java_repetition(agent5, agent2):
    interactions = [
        {"reelId": "R1", "watchPercentage": 90.0, "liked": True},
        {"reelId": "R2", "watchPercentage": 88.0, "liked": True},
    ]
    reel_analyses = {
        "R1": {"title": "Java Spring Boot Basics", "primaryTopic": "Java", "broaderDomain": "Software Engineering"},
        "R2": {"title": "Day in Life of SWE", "primaryTopic": "Software Engineering", "broaderDomain": "Software Engineering"},
    }
    profile = await agent2.infer("student_swe", interactions, reel_analyses)

    candidates = [
        {"candidateId": "CAND_JAVA_02", "title": "Java Syntax 101", "topic": "Java", "category": "Java", "candidateType": "Familiar", "novelty": 0.30},
        {"candidateId": "CAND_TECH003", "title": "REST APIs Explained: Design & Best Practices", "topic": "APIs", "category": "Backend", "candidateType": "Adjacent", "novelty": 0.88},
    ]

    quality_evals = [
        QualityAssessment(
            candidateId="CAND_JAVA_02", educationalValue=0.50, practicalUsefulness=0.50, technicalDepth=0.40,
            careerRelevance=0.40, evidenceQuality=0.50, entertainmentValue=0.60, hypeScore=0.10,
            clickbaitScore=0.10, promotionalScore=0.10, misleadingClaimRisk=0.0, qualityScore=0.60, decision=QualityDecision.ACCEPT
        ),
        QualityAssessment(
            candidateId="CAND_TECH003", educationalValue=0.90, practicalUsefulness=0.90, technicalDepth=0.85,
            careerRelevance=0.80, evidenceQuality=0.85, entertainmentValue=0.70, hypeScore=0.05,
            clickbaitScore=0.05, promotionalScore=0.05, misleadingClaimRisk=0.0, qualityScore=0.90, decision=QualityDecision.ACCEPT
        ),
    ]

    response = await agent5.rank(
        user_id="student_swe",
        current_reel_id="R1",
        candidates=candidates,
        quality_evaluations=quality_evals,
        interest_profile=profile,
        recently_consumed_topics=["Java", "Java"]
    )

    assert response.selectedRecommendation.candidateId == "CAND_TECH003"
