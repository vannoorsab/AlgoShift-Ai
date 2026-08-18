import time
import datetime
from typing import List, Dict, Any
from app.models.quality import QualityAssessment, QualityDecision, EvaluateCandidatesResponse
from app.scoring.quality_engine import ContentQualityScoringEngine
from app.core.logging import logger

class ContentQualityAgent:
    """
    Agent 4: ContentQualityAgent (v1.0)
    Trust & Safety Hype Shield evaluating candidates across 10 quality dimensions.
    Returns structured QualityAssessment with ACCEPT, PENALIZE, or REJECT decisions.
    """
    agent_name: str = "ContentQualityAgent"
    agent_version: str = "1.0"

    def __init__(self):
        self.quality_engine = ContentQualityScoringEngine()

    async def evaluate_batch(
        self,
        user_id: str,
        candidates: List[Dict[str, Any]]
    ) -> EvaluateCandidatesResponse:
        start_time = time.time()
        
        evaluations: List[QualityAssessment] = []
        accepted_count = 0
        penalized_count = 0
        rejected_count = 0

        for item in candidates:
            assessment = self.quality_engine.calculate_quality(item)
            evaluations.append(assessment)

            if assessment.decision == QualityDecision.ACCEPT:
                accepted_count += 1
            elif assessment.decision == QualityDecision.PENALIZE:
                penalized_count += 1
            else:
                rejected_count += 1

        duration_ms = int((time.time() - start_time) * 1000)
        logger.info(
            f"ContentQualityAgent evaluated {len(evaluations)} candidates for {user_id} in {duration_ms}ms "
            f"(ACCEPT={accepted_count}, PENALIZE={penalized_count}, REJECT={rejected_count})"
        )

        return EvaluateCandidatesResponse(
            success=True,
            evaluatedCount=len(evaluations),
            acceptedCount=accepted_count,
            penalizedCount=penalized_count,
            rejectedCount=rejected_count,
            evaluations=evaluations
        )
