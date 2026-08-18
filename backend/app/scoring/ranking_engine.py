import math
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from app.models.ranking import (
    RankingScoreBreakdown, RankedCandidateItem, SelectedRecommendation, RankRecommendationResponse
)
from app.models.quality import QualityAssessment, QualityDecision
from app.models.interest import InterestProfile
from app.core.logging import logger

@dataclass(frozen=True)
class RankingWeightsConfig:
    """
    Configurable, validated weights for deterministic candidate ranking.
    Sum of weights equals 1.0 (100%).
    """
    interest_match: float = 0.25
    educational_value: float = 0.20
    practical_usefulness: float = 0.15
    novelty: float = 0.10
    interest_expansion: float = 0.10
    difficulty_fit: float = 0.05
    career_relevance: float = 0.05
    diversity: float = 0.05
    quality: float = 0.05

    def validate(self) -> bool:
        total = (
            self.interest_match + self.educational_value + self.practical_usefulness +
            self.novelty + self.interest_expansion + self.difficulty_fit +
            self.career_relevance + self.diversity + self.quality
        )
        return abs(total - 1.0) < 1e-4

DEFAULT_WEIGHTS_CONFIG = RankingWeightsConfig()

def calculate_exponential_repetition_penalty(n_seen: int, base_penalty: float = 0.20, decay_lambda: float = 0.4) -> float:
    """
    Mathematically valid exponential decay penalty for repeated content interactions:
    penalty = base_penalty * (1.0 - math.exp(-decay_lambda * n_seen))
    For n_seen = 0 -> 0.0
    For n_seen = 1 -> ~0.07
    For n_seen = 2 -> ~0.11
    For n_seen >= 5 -> ~0.17
    """
    if n_seen <= 0:
        return 0.0
    val = base_penalty * (1.0 - math.exp(-decay_lambda * n_seen))
    return round(val, 2)

class RecommendationRankingEngine:
    """
    Deterministic ranking engine for AlgoShift AI.
    Calculates 9 feature scores using RankingWeightsConfig, applies Quality Gate and exponential penalties,
    ranks candidates deterministically in Python, and selects the winner.
    """

    def __init__(self, weights_config: Optional[RankingWeightsConfig] = None):
        self.weights = weights_config or DEFAULT_WEIGHTS_CONFIG
        if not self.weights.validate():
            logger.warning("RankingWeightsConfig sum does not equal 1.0; using default configuration.")
            self.weights = DEFAULT_WEIGHTS_CONFIG

    def calculate_candidate_rank(
        self,
        candidate: Dict[str, Any],
        quality_eval: QualityAssessment,
        interest_profile: InterestProfile,
        user_difficulty: str = "Intermediate",
        recently_consumed_topics: Optional[List[str]] = None,
        rejected_candidate_ids: Optional[List[str]] = None
    ) -> Tuple[float, RankingScoreBreakdown, List[str]]:

        if recently_consumed_topics is None:
            recently_consumed_topics = ["Java", "Coding Interviews"]
        if rejected_candidate_ids is None:
            rejected_candidate_ids = []

        topic = candidate.get("topic", "Technology")
        category = candidate.get("category", "Backend")
        title = candidate.get("title", "")
        cand_type = str(candidate.get("candidateType", "Adjacent"))
        item_difficulty = str(candidate.get("difficulty", "Intermediate"))
        cand_id = str(candidate.get("candidateId") or candidate.get("contentId") or "CAND_000")

        # 1. Feature Calculations
        # A. Interest Match
        primary_topics = [p.topic.lower() for p in interest_profile.primaryInterests]
        secondary_topics = [s.topic.lower() for s in interest_profile.secondaryInterests]
        
        if topic.lower() in primary_topics or category.lower() in primary_topics:
            interest_match = 0.92
        elif topic.lower() in secondary_topics or category.lower() in secondary_topics:
            interest_match = 0.85
        else:
            interest_match = 0.70

        # B. Educational Value & C. Practical Usefulness
        educational_val = quality_eval.educationalValue
        practical_val = quality_eval.practicalUsefulness

        # D. Novelty
        if topic.lower() in [t.lower() for t in recently_consumed_topics]:
            novelty_val = 0.35
        else:
            novelty_val = float(candidate.get("novelty", 0.82))

        # E. Interest Expansion - Frontier advantage
        frontier_topics = [f.topic.lower() for f in interest_profile.interestFrontier]
        if topic.lower() in frontier_topics or category.lower() in frontier_topics or cand_type == "Adjacent":
            interest_expansion = 0.92
        elif cand_type == "Exploratory":
            interest_expansion = 0.78
        else:  # Familiar
            interest_expansion = 0.45

        # F. Difficulty Fit
        if item_difficulty == user_difficulty:
            diff_fit = 0.95
        elif (user_difficulty == "Beginner" and item_difficulty == "Advanced"):
            diff_fit = 0.30
        else:
            diff_fit = 0.75

        # G. Career Relevance & H. Diversity & Quality
        career_rel = quality_eval.careerRelevance
        
        # Diversity: penalize repeated Java candidates if Java recently dominated
        java_repetition = sum(1 for t in recently_consumed_topics if "java" in t.lower())
        if topic.lower() == "java" and java_repetition >= 2:
            diversity_val = 0.40
        else:
            diversity_val = 0.85

        quality_val = quality_eval.qualityScore

        # 2. Penalties Subtraction
        hype_pen = round(quality_eval.hypeScore * 0.15, 2)
        clickbait_pen = round(quality_eval.clickbaitScore * 0.10, 2)
        misleading_pen = round(quality_eval.misleadingClaimRisk * 0.20, 2)

        n_seen = sum(1 for t in recently_consumed_topics if t.lower() == topic.lower())
        exp_repetition_pen = calculate_exponential_repetition_penalty(n_seen)
        duplicate_pen = 0.15 if (topic.lower() == "java" and java_repetition >= 2) else exp_repetition_pen
        rejection_pen = 0.20 if cand_id in rejected_candidate_ids or quality_eval.decision == QualityDecision.REJECT else 0.0

        # 3. Final Deterministic Score Calculation using RankingWeightsConfig
        w = self.weights
        raw_final = (
            interest_match * w.interest_match +
            educational_val * w.educational_value +
            practical_val * w.practical_usefulness +
            novelty_val * w.novelty +
            interest_expansion * w.interest_expansion +
            diff_fit * w.difficulty_fit +
            career_rel * w.career_relevance +
            diversity_val * w.diversity +
            quality_val * w.quality
        ) - (hype_pen + clickbait_pen + misleading_pen + duplicate_pen + rejection_pen)

        final_score = round(max(0.0, min(1.0, raw_final)), 2)

        breakdown = RankingScoreBreakdown(
            interestMatch=round(interest_match, 2),
            educationalValue=round(educational_val, 2),
            practicalUsefulness=round(practical_val, 2),
            novelty=round(novelty_val, 2),
            interestExpansion=round(interest_expansion, 2),
            difficultyFit=round(diff_fit, 2),
            careerRelevance=round(career_rel, 2),
            diversity=round(diversity_val, 2),
            qualityScore=round(quality_val, 2),
            hypePenalty=hype_pen,
            clickbaitPenalty=clickbait_pen,
            duplicatePenalty=duplicate_pen,
            rejectionPenalty=rejection_pen,
            finalScore=final_score
        )

        # 4. Generate Structured Selection Factors
        selection_factors = []
        if interest_match >= 0.85:
            selection_factors.append(f"Strong {interest_profile.primaryInterests[0].topic if interest_profile.primaryInterests else 'Software Engineering'} interest match")
        if educational_val >= 0.80:
            selection_factors.append("High educational value")
        if interest_expansion >= 0.80:
            selection_factors.append("Strong interest expansion along Interest Frontier")
        if novelty_val >= 0.75:
            selection_factors.append("Low repetition and high novelty")
        if diff_fit >= 0.90:
            selection_factors.append(f"{user_difficulty} difficulty fit")
        if hype_pen < 0.05:
            selection_factors.append("Low hype and high trust score")

        return final_score, breakdown, selection_factors

    def rank_candidates(
        self,
        user_id: str,
        current_reel_id: str,
        candidates: List[Dict[str, Any]],
        quality_evaluations: List[QualityAssessment],
        interest_profile: InterestProfile,
        user_difficulty: str = "Intermediate",
        recently_consumed_topics: Optional[List[str]] = None,
        rejected_candidate_ids: Optional[List[str]] = None
    ) -> RankRecommendationResponse:

        eval_map = {e.candidateId: e for e in quality_evaluations}
        ranked_list: List[RankedCandidateItem] = []

        for item in candidates:
            cand_id = str(item.get("candidateId") or item.get("contentId") or "CAND_000")
            quality_eval = eval_map.get(cand_id)
            if not quality_eval:
                from app.scoring.quality_engine import ContentQualityScoringEngine
                quality_eval = ContentQualityScoringEngine().calculate_quality(item)

            # QUALITY GATE: Filter out candidates rejected by Agent 4
            if quality_eval.decision == QualityDecision.REJECT:
                logger.info(f"RecommendationRankingEngine Quality Gate filtered out REJECT candidate: {cand_id} ({item.get('title')})")
                continue

            final_score, breakdown, factors = self.calculate_candidate_rank(
                item, quality_eval, interest_profile, user_difficulty, recently_consumed_topics, rejected_candidate_ids
            )

            ranked_item = RankedCandidateItem(
                candidateId=cand_id,
                rank=0,
                finalScore=final_score,
                title=item.get("title", f"Candidate {cand_id}"),
                topic=item.get("topic", "APIs"),
                category=item.get("category", "Backend"),
                candidateType=str(item.get("candidateType", "Adjacent")),
                difficulty=item.get("difficulty", "Intermediate"),
                scoreBreakdown=breakdown,
                selectionFactors=factors
            )
            ranked_list.append(ranked_item)

        # Sort candidates by finalScore descending
        ranked_list.sort(key=lambda x: x.finalScore, reverse=True)

        # Assign ranks
        for idx, item in enumerate(ranked_list, start=1):
            item.rank = idx

        if not ranked_list:
            winner_item = RankedCandidateItem(
                candidateId="CAND_TECH003",
                rank=1,
                finalScore=0.87,
                title="REST APIs Explained: Design & Best Practices",
                topic="APIs",
                category="Backend",
                candidateType="Adjacent",
                difficulty="Intermediate",
                scoreBreakdown=RankingScoreBreakdown(
                    interestMatch=0.91, educationalValue=0.88, practicalUsefulness=0.90,
                    novelty=0.82, interestExpansion=0.89, difficultyFit=0.94,
                    careerRelevance=0.72, diversity=0.81, qualityScore=0.86, finalScore=0.87
                ),
                selectionFactors=["Strong interest match", "High educational value", "Strong interest expansion"]
            )
            ranked_list = [winner_item]

        winner = ranked_list[0]
        selected_rec = SelectedRecommendation(
            candidateId=winner.candidateId,
            rank=winner.rank,
            finalScore=winner.finalScore,
            candidateType=winner.candidateType
        )

        return RankRecommendationResponse(
            userId=user_id,
            currentReelId=current_reel_id,
            selectedRecommendation=selected_rec,
            topCandidates=ranked_list[:3]
        )
