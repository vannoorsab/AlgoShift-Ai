import time
import datetime
import uuid
from typing import List, Dict, Any, Optional
from app.repositories.recommendation_repository import RecommendationRepository
from app.repositories.catalog_repository import CatalogRepository
from app.repositories.agent_run_repository import AgentRunRepository
from app.services.interest_service import InterestService
from app.agents.candidate_generation import CandidateGenerationAgent
from app.agents.content_quality import ContentQualityAgent
from app.agents.recommendation_ranking import RecommendationRankingAgent
from app.agents.explanation import ExplanationAgent
from app.agents.feedback_learning import FeedbackLearningAgent
from app.models.recommendation import (
    Recommendation, RejectedContent, CandidateGenerationResponse, CandidateItem
)
from app.models.quality import EvaluateCandidatesResponse, QualityAssessment
from app.models.ranking import RankRecommendationResponse, SelectedRecommendation, RankedCandidateItem
from app.models.explanation import ExplainRecommendationResponse, ChallengeExplanationResult, EvidenceTransparency
from app.models.feedback import RecommendationFeedbackPayload, RecommendationFeedbackResponse
from app.services.demo_dataset import DEMO_REELS
from app.services.seed_service import INITIAL_RECOMMENDATIONS
from app.core.logging import logger

class RecommendationService:
    def __init__(
        self,
        repo: Optional[RecommendationRepository] = None,
        catalog_repo: Optional[CatalogRepository] = None,
        agent_repo: Optional[AgentRunRepository] = None,
        interest_service: Optional[InterestService] = None
    ):
        self.repo = repo or RecommendationRepository()
        self.catalog_repo = catalog_repo or CatalogRepository()
        self.agent_repo = agent_repo or AgentRunRepository()
        self.interest_service = interest_service or InterestService()
        self.candidate_agent = CandidateGenerationAgent()
        self.quality_agent = ContentQualityAgent()
        self.ranking_agent = RecommendationRankingAgent()
        self.explanation_agent = ExplanationAgent()
        self.feedback_agent = FeedbackLearningAgent()

    async def generate_candidate_pool(
        self,
        user_id: str,
        user_difficulty: str = "Intermediate"
    ) -> CandidateGenerationResponse:
        start_time = time.time()
        now = datetime.datetime.utcnow().isoformat() + "Z"

        profile = await self.interest_service.infer_interests(user_id)
        catalog_items = await self.catalog_repo.get_all_items()

        try:
            response: CandidateGenerationResponse = await self.candidate_agent.generate_candidates(
                user_id=user_id,
                interest_profile=profile,
                catalog_items=catalog_items,
                user_difficulty=user_difficulty
            )
            duration_ms = int((time.time() - start_time) * 1000)

            candidate_run_doc = {
                "id": f"CAND_RUN_{uuid.uuid4().hex[:8]}",
                "userId": user_id,
                "candidateCount": response.candidateCount,
                "candidates": [c.model_dump() for c in response.candidates],
                "generationVersion": self.candidate_agent.agent_version,
                "createdAt": now
            }
            await self.repo.recommendations_repo.insert_one(candidate_run_doc)

            agent_run_doc = {
                "agentName": self.candidate_agent.agent_name,
                "agentVersion": self.candidate_agent.agent_version,
                "userId": user_id,
                "candidateCount": response.candidateCount,
                "status": "success",
                "durationMs": duration_ms,
                "createdAt": now
            }
            await self.agent_repo.insert_one(agent_run_doc)

            return response

        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            error_run_doc = {
                "agentName": self.candidate_agent.agent_name,
                "agentVersion": self.candidate_agent.agent_version,
                "userId": user_id,
                "status": "failure",
                "error": str(e),
                "durationMs": duration_ms,
                "createdAt": now
            }
            await self.agent_repo.insert_one(error_run_doc)
            raise e

    async def evaluate_candidate_quality(
        self,
        user_id: str,
        candidate_ids: Optional[List[str]] = None,
        custom_candidates: Optional[List[Dict[str, Any]]] = None
    ) -> EvaluateCandidatesResponse:
        start_time = time.time()
        now = datetime.datetime.utcnow().isoformat() + "Z"

        candidates_to_eval = []

        if custom_candidates:
            candidates_to_eval = custom_candidates
        elif candidate_ids:
            all_catalog = await self.catalog_repo.get_all_items()
            for cid in candidate_ids:
                match = next((item for item in all_catalog if item.get("contentId") == cid or item.get("candidateId") == cid), None)
                if match:
                    candidates_to_eval.append(match)
                else:
                    candidates_to_eval.append({"candidateId": cid, "title": f"Candidate {cid}", "description": ""})
        else:
            gen_res = await self.generate_candidate_pool(user_id)
            candidates_to_eval = [c.model_dump() for c in gen_res.candidates]

        try:
            response: EvaluateCandidatesResponse = await self.quality_agent.evaluate_batch(user_id, candidates_to_eval)
            duration_ms = int((time.time() - start_time) * 1000)

            eval_doc = {
                "id": f"EVAL_RUN_{uuid.uuid4().hex[:8]}",
                "userId": user_id,
                "evaluatedCount": response.evaluatedCount,
                "acceptedCount": response.acceptedCount,
                "penalizedCount": response.penalizedCount,
                "rejectedCount": response.rejectedCount,
                "evaluations": [e.model_dump() for e in response.evaluations],
                "evaluationVersion": self.quality_agent.agent_version,
                "createdAt": now
            }
            await self.repo.recommendations_repo.insert_one(eval_doc)

            agent_run_doc = {
                "agentName": self.quality_agent.agent_name,
                "agentVersion": self.quality_agent.agent_version,
                "userId": user_id,
                "candidateCount": response.evaluatedCount,
                "acceptedCount": response.acceptedCount,
                "penalizedCount": response.penalizedCount,
                "rejectedCount": response.rejectedCount,
                "status": "success",
                "durationMs": duration_ms,
                "createdAt": now
            }
            await self.agent_repo.insert_one(agent_run_doc)

            return response

        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            error_run_doc = {
                "agentName": self.quality_agent.agent_name,
                "agentVersion": self.quality_agent.agent_version,
                "userId": user_id,
                "status": "failure",
                "error": str(e),
                "durationMs": duration_ms,
                "createdAt": now
            }
            await self.agent_repo.insert_one(error_run_doc)
            raise e

    async def rank_recommendations(
        self,
        user_id: str,
        current_reel_id: str = "R003",
        custom_candidates: Optional[List[Dict[str, Any]]] = None
    ) -> RankRecommendationResponse:
        start_time = time.time()
        now = datetime.datetime.utcnow().isoformat() + "Z"

        profile = await self.interest_service.infer_interests(user_id)

        if custom_candidates:
            candidates = custom_candidates
        else:
            gen_res = await self.generate_candidate_pool(user_id)
            candidates = [c.model_dump() for c in gen_res.candidates]

        qual_res = await self.quality_agent.evaluate_batch(user_id, candidates)
        quality_evaluations = qual_res.evaluations

        try:
            response: RankRecommendationResponse = await self.ranking_agent.rank(
                user_id=user_id,
                current_reel_id=current_reel_id,
                candidates=candidates,
                quality_evaluations=quality_evaluations,
                interest_profile=profile
            )
            duration_ms = int((time.time() - start_time) * 1000)

            ranking_doc = {
                "id": f"RANK_RUN_{uuid.uuid4().hex[:8]}",
                "userId": user_id,
                "currentReelId": current_reel_id,
                "selectedCandidate": response.selectedRecommendation.model_dump(),
                "topCandidates": [c.model_dump() for c in response.topCandidates],
                "rankingVersion": self.ranking_agent.agent_version,
                "createdAt": now
            }
            await self.repo.recommendations_repo.insert_one(ranking_doc)

            agent_run_doc = {
                "agentName": self.ranking_agent.agent_name,
                "agentVersion": self.ranking_agent.agent_version,
                "userId": user_id,
                "candidateCount": len(candidates),
                "selectedCandidateId": response.selectedRecommendation.candidateId,
                "status": "success",
                "durationMs": duration_ms,
                "createdAt": now
            }
            await self.agent_repo.insert_one(agent_run_doc)

            return response

        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            error_run_doc = {
                "agentName": self.ranking_agent.agent_name,
                "agentVersion": self.ranking_agent.agent_version,
                "userId": user_id,
                "status": "failure",
                "error": str(e),
                "durationMs": duration_ms,
                "createdAt": now
            }
            await self.agent_repo.insert_one(error_run_doc)
            raise e

    async def explain_recommendation(
        self,
        user_id: str,
        current_reel_id: str = "R003"
    ) -> ExplainRecommendationResponse:
        start_time = time.time()
        now = datetime.datetime.utcnow().isoformat() + "Z"

        current_reel = {}
        if current_reel_id in DEMO_REELS:
            c = DEMO_REELS[current_reel_id]
            current_reel = {"reelId": c.reelId, "title": c.title}
        else:
            current_reel = {"reelId": current_reel_id, "title": "Coding Interview Joke"}

        profile = await self.interest_service.infer_interests(user_id)
        ranking_response = await self.rank_recommendations(user_id, current_reel_id)

        try:
            response: ExplainRecommendationResponse = await self.explanation_agent.explain(
                user_id=user_id,
                current_reel=current_reel,
                interest_profile=profile,
                ranking_response=ranking_response
            )
            duration_ms = int((time.time() - start_time) * 1000)

            result_doc = {
                "id": f"EXPLAIN_RUN_{uuid.uuid4().hex[:8]}",
                "userId": user_id,
                "currentReelId": current_reel_id,
                "result": response.result.model_dump(),
                "evidence": response.evidence.model_dump(),
                "explanationVersion": self.explanation_agent.agent_version,
                "createdAt": now
            }
            await self.repo.recommendations_repo.insert_one(result_doc)

            agent_run_doc = {
                "agentName": self.explanation_agent.agent_name,
                "agentVersion": self.explanation_agent.agent_version,
                "userId": user_id,
                "currentReelId": current_reel_id,
                "status": "success",
                "durationMs": duration_ms,
                "confidence": response.result.confidence,
                "createdAt": now
            }
            await self.agent_repo.insert_one(agent_run_doc)

            return response

        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            error_run_doc = {
                "agentName": self.explanation_agent.agent_name,
                "agentVersion": self.explanation_agent.agent_version,
                "userId": user_id,
                "currentReelId": current_reel_id,
                "status": "failure",
                "error": str(e),
                "durationMs": duration_ms,
                "createdAt": now
            }
            await self.agent_repo.insert_one(error_run_doc)
            raise e

    async def process_recommendation_feedback(
        self,
        payload: RecommendationFeedbackPayload
    ) -> RecommendationFeedbackResponse:
        current_profile = await self.interest_service.infer_interests(payload.userId)
        return await self.feedback_agent.process_feedback(payload, current_profile)

    async def get_user_recommendations(self, user_id: str) -> List[Recommendation]:
        docs = await self.repo.get_user_recommendations(user_id)
        if docs:
            return [Recommendation(**d) for d in docs if "title" in d]
        return [Recommendation(**d) for d in INITIAL_RECOMMENDATIONS]

    async def generate_recommendations(self, user_id: str) -> List[Recommendation]:
        return await self.get_user_recommendations(user_id)

    async def handle_feedback(self, recommendation_id: str, feedback_type: str, reason: Optional[str] = None):
        return await self.repo.save_feedback(recommendation_id, feedback_type, reason)

    async def get_rejected_content(self, user_id: str) -> List[RejectedContent]:
        return [
            RejectedContent(
                id="rej1",
                title="10 AI Tools That Will Get You A Job",
                hypeScore=94,
                educationalValue=31,
                evidenceQuality=30,
                reason="Exaggerated career promise and high hype framing."
            ),
            RejectedContent(
                id="rej2",
                title="Learn Coding in 7 Days and Earn $10,000 a Month",
                hypeScore=95,
                educationalValue=20,
                evidenceQuality=15,
                reason="Unrealistic income promise and misleading claim risk."
            )
        ]
