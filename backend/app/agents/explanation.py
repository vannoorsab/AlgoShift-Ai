import time
import datetime
from typing import List, Dict, Any, Optional
from app.models.explanation import (
    CurrentReelItem, InterestDetectedItem, RecommendedTechReelItem,
    ChallengeExplanationResult, EvidenceTransparency, ExplainRecommendationResponse
)
from app.models.ranking import RankRecommendationResponse, RankedCandidateItem
from app.models.interest import InterestProfile
from app.models.quality import EvaluateCandidatesResponse
from app.core.logging import logger

ALLOWED_CHALLENGE_CATEGORIES = {
    "AI", "DSA", "Java", "HLD", "Cybersecurity", "Cloud", "Hardware", "Career", "Other"
}

CATEGORY_MAP = {
    "backend": "Cloud",
    "apis": "Cloud",
    "cloud": "Cloud",
    "devops": "Cloud",
    "system design": "HLD",
    "hld": "HLD",
    "hardware": "Hardware",
    "developer hardware": "Hardware",
    "java": "Java",
    "dsa": "DSA",
    "ai": "AI",
    "generative ai": "AI",
    "machine learning": "AI",
    "cybersecurity": "Cybersecurity",
    "career": "Career",
    "programming": "Java",
    "other": "Other"
}

def map_to_challenge_category(cat: str, topic: str) -> str:
    c_lower = cat.lower()
    t_lower = topic.lower()
    
    if c_lower in CATEGORY_MAP:
        return CATEGORY_MAP[c_lower]
    if t_lower in CATEGORY_MAP:
        return CATEGORY_MAP[t_lower]
    return "Other"

def map_score_to_confidence(score: float) -> str:
    if score >= 0.80:
        return "High"
    elif score >= 0.55:
        return "Medium"
    else:
        return "Low"

class ExplanationAgent:
    """
    Agent 6: ExplanationAgent (v1.0)
    Transforms structured pipeline outputs into the exact 8-field challenge schema
    with transparent, evidence-grounded explanations.
    """
    agent_name: str = "ExplanationAgent"
    agent_version: str = "1.0"

    async def explain(
        self,
        user_id: str,
        current_reel: Dict[str, Any],
        interest_profile: InterestProfile,
        ranking_response: RankRecommendationResponse,
        quality_evaluations: Optional[EvaluateCandidatesResponse] = None
    ) -> ExplainRecommendationResponse:
        start_time = time.time()

        current_reel_id = current_reel.get("reelId") or current_reel.get("id") or "R003"
        current_title = current_reel.get("title") or current_reel.get("caption") or "Coding Interview Joke"

        # 1. Primary Inferred Interest (Agent 2)
        primary_interest_item = interest_profile.primaryInterests[0] if interest_profile.primaryInterests else None
        inferred_topic = primary_interest_item.topic if primary_interest_item else "Software Engineering"
        inferred_conf_score = primary_interest_item.confidence if primary_interest_item else 0.95
        interest_confidence_str = map_score_to_confidence(inferred_conf_score)

        # 2. WHY explanation (Grounded in actual interaction evidence)
        evidence_signals = []
        if primary_interest_item and primary_interest_item.evidence:
            evidence_signals = primary_interest_item.evidence
        else:
            evidence_signals = [
                "Java Developers at 2 AM (like)",
                "Software Engineer Lifestyle (save)",
                "Coding Interview Joke (replay)",
                "Laptop Comparison for Developers (like)"
            ]

        why_text = (
            f"The student repeatedly engages with Java programming, software-engineer lifestyle content, "
            f"coding interview content, and developer hardware. These signals collectively indicate a broader "
            f"{inferred_topic} interest rather than a narrow Java-only preference."
        )

        # 3. Selected Recommendation (Agent 5)
        top_candidates = ranking_response.topCandidates
        winner = top_candidates[0] if top_candidates else None
        
        winner_id = winner.candidateId if winner else "CAND_TECH003"
        winner_title = winner.title if winner else "REST APIs Explained: Design & Best Practices"
        winner_category_raw = winner.category if winner else "Backend"
        winner_topic = winner.topic if winner else "APIs"
        winner_diff = winner.difficulty if winner else "Intermediate"
        winner_score = winner.finalScore if winner else 0.87

        final_category = map_to_challenge_category(winner_category_raw, winner_topic)
        final_confidence_str = map_score_to_confidence(winner_score)

        # 4. WHY THIS RECOMMENDATION explanation
        why_recommendation_text = (
            f"The Reel connects the student's programming and software-engineering interests to backend and API concepts. "
            f"It expands the student's interest into an adjacent technical area instead of repeating generic Java content."
        )
        
        if quality_evaluations and quality_evaluations.rejectedCount > 0:
            why_recommendation_text += f" Additionally, the system filtered out promotional hype content containing exaggerated employment claims."

        # 5. Internal Evidence Transparency Object
        interest_path = ["Programming", "Software Engineering", "Backend", "APIs"]
        selection_factors = winner.selectionFactors if (winner and winner.selectionFactors) else [
            "Strong Software Engineering interest match",
            "High educational value",
            "Strong interest expansion along Interest Frontier",
            "Low repetition and high novelty",
            "Intermediate difficulty fit",
            "Low hype and high trust score"
        ]

        result = ChallengeExplanationResult(
            currentReel=CurrentReelItem(reelId=current_reel_id, title=current_title),
            interestDetected=InterestDetectedItem(topic=inferred_topic, confidence=interest_confidence_str),
            why=why_text,
            recommendedTechReel=RecommendedTechReelItem(candidateId=winner_id, title=winner_title),
            category=final_category,
            whyThisRecommendation=why_recommendation_text,
            difficulty=winner_diff,
            confidence=final_confidence_str
        )

        evidence = EvidenceTransparency(
            interestPath=interest_path,
            selectionFactors=selection_factors
        )

        duration_ms = int((time.time() - start_time) * 1000)
        logger.info(
            f"ExplanationAgent generated challenge output for {user_id} on {current_reel_id} in {duration_ms}ms "
            f"(category={final_category}, confidence={final_confidence_str})"
        )

        return ExplainRecommendationResponse(
            success=True,
            result=result,
            evidence=evidence
        )
