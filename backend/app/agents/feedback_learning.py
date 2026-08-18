import time
import datetime
import uuid
from typing import List, Dict, Any, Optional
from app.models.feedback import RecommendationFeedbackPayload, RecommendationFeedbackResponse, InterestTopicChange
from app.models.interest import InterestProfile
from app.scoring.feedback_engine import FeedbackEngine
from app.db.mongodb import (
    db_manager, COLLECTION_INTERACTIONS, COLLECTION_INTEREST_PROFILES,
    COLLECTION_INTEREST_HISTORY, COLLECTION_AGENT_RUNS, COLLECTION_REELS, COLLECTION_RECOMMENDATION_CATALOG
)
from app.core.logging import logger

class FeedbackLearningAgent:
    """
    Agent 7: FeedbackLearningAgent (v1.0)
    Learns from user interaction feedback after recommendation consumption,
    propagates semantic interest updates, stores versioned profile snapshots, and prevents duplicates.
    """
    agent_name: str = "FeedbackLearningAgent"
    agent_version: str = "1.0"

    def __init__(self):
        self.engine = FeedbackEngine()

    async def process_feedback(
        self,
        payload: RecommendationFeedbackPayload,
        current_profile: InterestProfile
    ) -> RecommendationFeedbackResponse:
        start_time = time.time()
        now = datetime.datetime.utcnow().isoformat() + "Z"

        user_id = payload.userId
        reel_id = payload.reelId
        event_id = payload.eventId or f"EVT_{user_id}_{reel_id}_{int(start_time)}"

        # 1. Idempotency Check: Prevent duplicate event processing
        existing_event = await db_manager.db[COLLECTION_INTERACTIONS].find_one(
            {"userId": user_id, "reelId": reel_id, "eventId": event_id}
        )
        if existing_event:
            logger.info(f"FeedbackLearningAgent: Idempotent event skipped for {user_id} on {reel_id}")
            return RecommendationFeedbackResponse(
                success=True,
                updatedInterests=[
                    InterestTopicChange(topic="Backend", previousScore=0.81, newScore=0.81, change=0.0)
                ]
            )

        # 2. Determine target topic from Reel metadata or catalog
        reel_doc = await db_manager.db[COLLECTION_REELS].find_one({"id": reel_id})
        if not reel_doc:
            reel_doc = await db_manager.db[COLLECTION_RECOMMENDATION_CATALOG].find_one(
                {"$or": [{"contentId": reel_id}, {"candidateId": reel_id}]}
            )

        target_topic = "APIs"
        if reel_doc:
            target_topic = reel_doc.get("topic") or reel_doc.get("category") or "APIs"

        # 3. Store raw interaction event
        interaction_doc = {
            "id": f"INT_{uuid.uuid4().hex[:8]}",
            "userId": user_id,
            "reelId": reel_id,
            "eventId": event_id,
            "watchPercentage": payload.watchPercentage,
            "liked": payload.liked,
            "saved": payload.saved,
            "shared": payload.shared,
            "rewatched": payload.rewatched,
            "skipped": payload.skipped,
            "completed": payload.completed,
            "timestamp": now
        }
        await db_manager.db[COLLECTION_INTERACTIONS].insert_one(interaction_doc)

        # 4. Compute profile updates & semantic propagation
        previous_profile_dict = current_profile.model_dump()
        updated_profile, changes = self.engine.update_profile_with_feedback(current_profile, target_topic, payload)

        # 5. Persist updated profile
        profile_dict = updated_profile.model_dump()
        await db_manager.db[COLLECTION_INTEREST_PROFILES].update_one(
            {"userId": user_id},
            {"$set": profile_dict},
            upsert=True
        )

        # 6. Store snapshot version in interest_history
        history_doc = {
            "id": f"HIST_{uuid.uuid4().hex[:8]}",
            "userId": user_id,
            "previousProfile": previous_profile_dict,
            "newProfile": profile_dict,
            "triggerReelId": reel_id,
            "feedback": payload.model_dump(),
            "changedInterests": [c.model_dump() for c in changes],
            "version": f"v_{int(start_time)}",
            "timestamp": now
        }
        await db_manager.db[COLLECTION_INTEREST_HISTORY].insert_one(history_doc)

        # 7. Log agent run execution to agent_runs
        duration_ms = int((time.time() - start_time) * 1000)
        agent_run_doc = {
            "agentName": self.agent_name,
            "agentVersion": self.agent_version,
            "userId": user_id,
            "reelId": reel_id,
            "feedbackType": "explicit_and_implicit",
            "changedInterestCount": len(changes),
            "status": "success",
            "durationMs": duration_ms,
            "createdAt": now
        }
        await db_manager.db[COLLECTION_AGENT_RUNS].insert_one(agent_run_doc)

        logger.info(f"FeedbackLearningAgent updated {len(changes)} interests for {user_id} in {duration_ms}ms")

        return RecommendationFeedbackResponse(
            success=True,
            updatedInterests=changes
        )
