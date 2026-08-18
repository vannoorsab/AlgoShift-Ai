from typing import Dict, Any, List, Tuple, Optional
from app.models.feedback import RecommendationFeedbackPayload, InterestTopicChange
from app.models.interest import InterestProfile, InterestItem, FrontierItem

SEMANTIC_PROPAGATION_MAP = {
    "apis": [("Backend", 0.7), ("Software Engineering", 0.4), ("Programming", 0.2)],
    "backend": [("APIs", 0.7), ("Software Engineering", 0.5), ("Programming", 0.3)],
    "databases": [("Backend", 0.7), ("Software Engineering", 0.4)],
    "cloud": [("DevOps", 0.7), ("Software Engineering", 0.4)],
    "system design": [("Software Engineering", 0.7), ("Backend", 0.5)],
    "java": [("Programming", 0.7), ("Software Engineering", 0.4)],
    "gaming": [("Software Engineering", 0.2)]
}

class FeedbackEngine:
    """
    Deterministic feedback scoring and semantic propagation engine for Agent 7.
    """

    def compute_action_score(self, payload: RecommendationFeedbackPayload) -> float:
        score = 0.0

        if payload.skipped:
            score += -1.0

        wp = payload.watchPercentage or 0.0
        if wp < 25.0:
            score += -0.5
        elif 25.0 <= wp < 50.0:
            score += 0.0
        elif 50.0 <= wp < 80.0:
            score += 0.5
        elif wp >= 80.0:
            score += 1.0

        if payload.completed:
            score += 1.0
        if payload.rewatched:
            score += 1.5
        if payload.liked:
            score += 2.0
        if payload.saved:
            score += 3.0
        if payload.shared:
            score += 3.0

        return score

    def update_profile_with_feedback(
        self,
        profile: InterestProfile,
        target_topic: str,
        payload: RecommendationFeedbackPayload
    ) -> Tuple[InterestProfile, List[InterestTopicChange]]:

        raw_score = self.compute_action_score(payload)
        base_delta = round(raw_score * 0.04, 2)

        changes: List[InterestTopicChange] = []
        topic_lower = target_topic.lower()

        # Update direct target topic score
        prev_map = {item.topic.lower(): item for item in profile.primaryInterests + profile.secondaryInterests + profile.emergingInterests}
        
        target_item = prev_map.get(topic_lower)
        prev_score = target_item.score if target_item else 0.60
        new_score = round(max(0.05, min(0.99, prev_score + base_delta)), 2)

        if target_item:
            target_item.score = new_score
        else:
            profile.primaryInterests.append(InterestItem(topic=target_topic, score=new_score, confidence=0.80, evidence=["feedback"]))

        changes.append(InterestTopicChange(
            topic=target_topic,
            previousScore=prev_score,
            newScore=new_score,
            change=round(new_score - prev_score, 2)
        ))

        # Semantic Propagation to related topics
        propagations = SEMANTIC_PROPAGATION_MAP.get(topic_lower, [])
        for rel_topic, scale in propagations:
            rel_lower = rel_topic.lower()
            rel_item = prev_map.get(rel_lower)
            rel_prev = rel_item.score if rel_item else 0.50
            rel_delta = round(base_delta * scale, 2)
            rel_new = round(max(0.05, min(0.99, rel_prev + rel_delta)), 2)

            if rel_item:
                rel_item.score = rel_new
            else:
                profile.primaryInterests.append(InterestItem(topic=rel_topic, score=rel_new, confidence=0.75, evidence=["semantic_propagation"]))

            changes.append(InterestTopicChange(
                topic=rel_topic,
                previousScore=rel_prev,
                newScore=rel_new,
                change=round(rel_new - rel_prev, 2)
            ))

        # Negative feedback handling
        if base_delta < 0:
            if target_topic not in profile.decliningInterests:
                profile.decliningInterests.append(target_topic)

        # Exploration protection: ensure frontier topics are preserved
        existing_frontier_topics = [f.topic for f in profile.interestFrontier]
        core_frontier = ["Backend", "APIs", "Databases", "Cloud", "System Design"]
        for cf in core_frontier:
            if cf not in existing_frontier_topics:
                profile.interestFrontier.append(FrontierItem(topic=cf, score=0.80))

        # Re-sort primary interests by score
        profile.primaryInterests.sort(key=lambda x: x.score, reverse=True)

        return profile, changes
