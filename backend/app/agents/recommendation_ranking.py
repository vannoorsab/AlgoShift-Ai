import time
import datetime
from typing import List, Dict, Any, Optional
from app.models.ranking import RankRecommendationResponse
from app.models.quality import QualityAssessment
from app.models.interest import InterestProfile
from app.scoring.ranking_engine import RecommendationRankingEngine
from app.core.logging import logger

class RecommendationRankingAgent:
    """
    Agent 5: RecommendationRankingAgent (v1.0)
    Selects the best next technology Reel from the quality-filtered candidate pool
    by balancing interest relevance, educational value, usefulness, novelty, and interest expansion.
    """
    agent_name: str = "RecommendationRankingAgent"
    agent_version: str = "1.0"

    def __init__(self):
        self.ranking_engine = RecommendationRankingEngine()

    async def rank(
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
        start_time = time.time()

        response = self.ranking_engine.rank_candidates(
            user_id=user_id,
            current_reel_id=current_reel_id,
            candidates=candidates,
            quality_evaluations=quality_evaluations,
            interest_profile=interest_profile,
            user_difficulty=user_difficulty,
            recently_consumed_topics=recently_consumed_topics,
            rejected_candidate_ids=rejected_candidate_ids
        )

        duration_ms = int((time.time() - start_time) * 1000)
        logger.info(
            f"RecommendationRankingAgent selected winner {response.selectedRecommendation.candidateId} "
            f"(rank=1, finalScore={response.selectedRecommendation.finalScore}) for {user_id} in {duration_ms}ms"
        )
        return response
