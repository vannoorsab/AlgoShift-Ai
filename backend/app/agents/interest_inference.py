import time
import datetime
from typing import List, Dict, Any, Tuple
from app.models.interest import (
    InterestProfile, InterestItem, WeakSignalItem, NegativeSignalItem,
    CuriosityItem, FrontierItem
)
from app.scoring.behavioral_engine import BehavioralScoringEngine
from app.agents.taxonomy import DOMAIN_HIERARCHY, TAXONOMY_DOMAINS
from app.core.logging import logger

FRONTIER_MAP = {
    "Software Engineering": [
        ("Backend", 0.78),
        ("APIs", 0.74),
        ("Cloud", 0.61),
        ("Databases", 0.68),
        ("System Design", 0.72)
    ],
    "Java": [
        ("Backend", 0.75),
        ("APIs", 0.70),
        ("System Design", 0.65)
    ],
    "Cloud": [
        ("DevOps", 0.70),
        ("Kubernetes", 0.65),
        ("Networking", 0.60)
    ],
    "AI": [
        ("Generative AI", 0.75),
        ("Machine Learning", 0.70),
        ("AI Agents", 0.68)
    ]
}

class InterestInferenceAgent:
    """
    Agent 2: InterestInferenceAgent (v1.0)
    Infers student's underlying interests, curiosity, contradiction signals,
    and interest frontier from interaction history & Reel analyses.
    """
    agent_name: str = "InterestInferenceAgent"
    agent_version: str = "1.0"

    def __init__(self, lambda_decay: float = 0.1):
        self.scoring_engine = BehavioralScoringEngine(lambda_decay=lambda_decay)

    async def infer_interests(self, user_id: str) -> InterestProfile:
        from app.services.interest_service import InterestService
        return await InterestService().infer_interests(user_id)

    async def infer(
        self,
        user_id: str,
        interactions: List[Dict[str, Any]],
        reel_analyses: Dict[str, Dict[str, Any]]
    ) -> InterestProfile:
        start_time = time.time()
        now = datetime.datetime.utcnow().isoformat() + "Z"

        if not interactions:
            return InterestProfile(
                userId=user_id,
                overallConfidence=0.0,
                updatedAt=now
            )

        domain_scores: Dict[str, float] = {}
        domain_active: Dict[str, float] = {}
        domain_counts: Dict[str, int] = {}
        domain_evidence: Dict[str, List[str]] = {}
        domain_skips: Dict[str, int] = {}
        domain_curiosity: Dict[str, float] = {}
        domain_timestamps: Dict[str, List[str]] = {}

        for inter in interactions:
            reel_id = inter.get("reelId", "")
            analysis = reel_analyses.get(reel_id, {})
            
            primary_topic = analysis.get("primaryTopic", "Technology")
            broader_domain = analysis.get("broaderDomain", DOMAIN_HIERARCHY.get(primary_topic, "Technology"))
            subtopics = analysis.get("subtopics", [])
            reel_title = analysis.get("title", f"Reel {reel_id}")
            
            score_meta = self.scoring_engine.calculate_interaction_score(inter)
            weighted_score = score_meta["weighted_score"]
            raw_total = score_meta["total_raw"]
            active_score = score_meta["active_score"]
            recency = score_meta["recency_weight"]
            watch_pct = float(inter.get("watchPercentage", 0))

            target_domains = [(broader_domain, 1.0)]
            if primary_topic != broader_domain:
                target_domains.append((primary_topic, 0.7))
            for st in subtopics[:2]:
                if st not in [broader_domain, primary_topic]:
                    target_domains.append((st, 0.5))

            for domain, weight_factor in target_domains:
                if domain not in domain_scores:
                    domain_scores[domain] = 0.0
                    domain_active[domain] = 0.0
                    domain_counts[domain] = 0
                    domain_evidence[domain] = []
                    domain_skips[domain] = 0
                    domain_curiosity[domain] = 0.0
                    domain_timestamps[domain] = []

                domain_scores[domain] += weighted_score * weight_factor
                domain_active[domain] += active_score * weight_factor
                domain_counts[domain] += 1
                domain_timestamps[domain].append(inter.get("timestamp", ""))

                if inter.get("action") == "skip" or watch_pct < 25.0:
                    domain_skips[domain] += 1

                if watch_pct >= 40.0 and active_score == 0:
                    curiosity_val = min(1.0, (watch_pct / 100.0) * recency)
                    domain_curiosity[domain] = max(domain_curiosity[domain], curiosity_val)

                if raw_total > 0:
                    action_str = inter.get("action", "engaged with")
                    ev_text = f"Strong engagement with {reel_title} ({action_str})"
                    if ev_text not in domain_evidence[domain]:
                        domain_evidence[domain].append(ev_text)

        primary_interests: List[InterestItem] = []
        secondary_interests: List[InterestItem] = []
        emerging_interests: List[InterestItem] = []
        declining_interests: List[InterestItem] = []
        weak_signals: List[WeakSignalItem] = []
        negative_signals: List[NegativeSignalItem] = []
        curiosity_list: List[CuriosityItem] = []

        max_raw_score = max(domain_scores.values()) if domain_scores else 1.0
        if max_raw_score <= 0:
            max_raw_score = 1.0

        for domain, raw_score in domain_scores.items():
            count = domain_counts[domain]
            skips = domain_skips[domain]
            act_score = domain_active[domain]
            
            norm_score = min(1.0, max(0.0, raw_score / max_raw_score))
            consistency = (count - skips) / max(1, count)
            conf = min(0.95, max(0.20, (0.5 * consistency + 0.3 * min(1.0, count / 3.0) + 0.2 * min(1.0, act_score / 4.0))))
            
            if skips > 0 and count > 1:
                conf *= 0.75

            is_single_passive = (count == 1 and act_score == 0)

            if raw_score <= -0.5 or (skips >= count and count >= 1 and act_score == 0):
                neg_score = min(1.0, max(0.1, abs(raw_score) / 3.0))
                negative_signals.append(NegativeSignalItem(
                    topic=domain,
                    score=round(neg_score, 2),
                    reason="Repeated low completion and skip behavior"
                ))
            elif norm_score < 0.45 or (is_single_passive and norm_score < 0.7):
                weak_signals.append(WeakSignalItem(
                    topic=domain,
                    score=round(norm_score, 2),
                    reason="Moderate watch but limited active engagement"
                ))
            else:
                ev_list = domain_evidence[domain] if domain_evidence[domain] else [f"Watched {domain} content"]
                trend_val = "Stable"
                if count == 1:
                    trend_val = "Emerging"
                elif count >= 3:
                    trend_val = "Stable"

                item = InterestItem(
                    topic=domain,
                    score=round(norm_score, 2),
                    confidence=round(conf, 2),
                    trend=trend_val,
                    evidence=ev_list
                )

                if norm_score >= 0.85 and not is_single_passive:
                    primary_interests.append(item)
                elif norm_score >= 0.65 and not is_single_passive:
                    secondary_interests.append(item)
                else:
                    emerging_interests.append(item)

            if domain_curiosity[domain] > 0.4 and act_score == 0:
                curiosity_list.append(CuriosityItem(
                    topic=domain,
                    score=round(domain_curiosity[domain], 2)
                ))

        primary_interests.sort(key=lambda x: x.score, reverse=True)
        secondary_interests.sort(key=lambda x: x.score, reverse=True)
        emerging_interests.sort(key=lambda x: x.score, reverse=True)
        weak_signals.sort(key=lambda x: x.score, reverse=True)
        negative_signals.sort(key=lambda x: x.score, reverse=True)
        curiosity_list.sort(key=lambda x: x.score, reverse=True)

        frontier_set: Dict[str, float] = {}
        all_consumed = set(domain_scores.keys())
        top_interests = primary_interests + secondary_interests
        
        for item in top_interests:
            candidates = FRONTIER_MAP.get(item.topic, [])
            for cand_topic, cand_score in candidates:
                if cand_topic not in all_consumed:
                    frontier_set[cand_topic] = max(frontier_set.get(cand_topic, 0.0), cand_score)

        interest_frontier = [
            FrontierItem(topic=t, score=round(s, 2))
            for t, s in sorted(frontier_set.items(), key=lambda x: x[1], reverse=True)
        ]

        if primary_interests:
            overall_conf = primary_interests[0].confidence
        elif secondary_interests:
            overall_conf = secondary_interests[0].confidence
        elif emerging_interests:
            overall_conf = emerging_interests[0].confidence
        else:
            overall_conf = 0.50

        profile = InterestProfile(
            userId=user_id,
            primaryInterests=primary_interests,
            secondaryInterests=secondary_interests,
            emergingInterests=emerging_interests,
            decliningInterests=declining_interests,
            weakSignals=weak_signals,
            negativeSignals=negative_signals,
            curiosity=curiosity_list,
            interestFrontier=interest_frontier,
            overallConfidence=round(overall_conf, 2),
            updatedAt=now
        )

        duration_ms = int((time.time() - start_time) * 1000)
        logger.info(f"InterestInferenceAgent inferred profile for {user_id} in {duration_ms}ms (overallConfidence={profile.overallConfidence})")
        return profile
