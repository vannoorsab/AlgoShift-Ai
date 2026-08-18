import time
import datetime
from typing import List, Dict, Any, Tuple, Optional
from app.models.recommendation import CandidateItem, CandidateType, CandidateGenerationResponse
from app.models.interest import InterestProfile, InterestItem
from app.models.enums import Difficulty
from app.agents.taxonomy import DOMAIN_HIERARCHY
from app.core.logging import logger

GRAPH_PATHS = {
    "Java": ["Programming", "Software Engineering", "Backend", "Java"],
    "APIs": ["Programming", "Software Engineering", "Backend", "APIs"],
    "Databases": ["Programming", "Software Engineering", "Backend", "Databases"],
    "System Design": ["Programming", "Software Engineering", "Backend", "System Design"],
    "Cloud": ["Programming", "Software Engineering", "Cloud"],
    "DevOps": ["Programming", "Software Engineering", "Cloud", "DevOps"],
    "Cybersecurity": ["Programming", "Software Engineering", "Cybersecurity"],
    "DSA": ["Programming", "DSA"],
    "AI": ["Programming", "Software Engineering", "AI"],
    "Hardware": ["Technology", "Hardware"],
    "Career": ["Technology", "Career"],
    "Gaming": ["Technology", "Gaming"],
    "Python": ["Programming", "Python"]
}

class CandidateGenerationAgent:
    """
    Agent 3: CandidateGenerationAgent (v1.0)
    Generates 10–20 candidates across Familiar, Adjacent, and Exploratory types
    using the Interest Frontier without performing final ranking.
    """
    agent_name: str = "CandidateGenerationAgent"
    agent_version: str = "1.0"

    def __init__(self, target_candidate_count: int = 12):
        self.target_candidate_count = target_candidate_count

    async def generate_candidates(
        self,
        user_id: str,
        interest_profile: InterestProfile,
        catalog_items: List[Dict[str, Any]],
        consumed_topics: Optional[List[str]] = None,
        user_difficulty: str = "Intermediate"
    ) -> CandidateGenerationResponse:
        start_time = time.time()
        
        if consumed_topics is None:
            consumed_topics = ["Java", "Coding Interviews", "Software Engineer Lifestyle", "Laptop Comparison"]

        primary_topics = [p.topic for p in interest_profile.primaryInterests]
        secondary_topics = [s.topic for s in interest_profile.secondaryInterests]
        frontier_topics = [f.topic for f in interest_profile.interestFrontier]
        negative_topics = [n.topic for n in interest_profile.negativeSignals]
        curiosity_topics = [c.topic for c in interest_profile.curiosity]

        primary_set = {p.lower() for p in primary_topics}
        secondary_set = {s.lower() for s in secondary_topics}
        frontier_set = {f.lower() for f in frontier_topics}
        negative_set = {n.lower() for n in negative_topics}

        # 1. Filter out items matching negative signals (e.g. Gaming)
        eligible_items = []
        for item in catalog_items:
            item_topic = item.get("topic", "")
            item_category = item.get("category", "")
            item_tags = [t.lower() for t in item.get("topics", [])] + [item_topic.lower(), item_category.lower()]
            
            if any(t in negative_set for t in item_tags):
                logger.info(f"CandidateGenerationAgent suppressed negative signal item: {item['title']} ({item_topic})")
                continue
            eligible_items.append(item)

        # 2. Score and classify candidates into Familiar, Adjacent, and Exploratory
        familiar_candidates: List[CandidateItem] = []
        adjacent_candidates: List[CandidateItem] = []
        exploratory_candidates: List[CandidateItem] = []
        
        seen_titles = set()

        for item in eligible_items:
            title = item.get("title", "")
            if title in seen_titles:
                continue
            seen_titles.add(title)

            topic = item.get("topic", "Technology")
            category = item.get("category", "Backend")
            item_difficulty_str = item.get("difficulty", "Intermediate")
            item_tags = [t.lower() for t in item.get("topics", [])] + [topic.lower(), category.lower()]
            
            # Explainable Path Traversal
            interest_path = GRAPH_PATHS.get(topic, GRAPH_PATHS.get(category, ["Programming", "Software Engineering", topic]))

            # Novelty Score Calculation (reduced for heavily consumed topics like Java)
            if topic in consumed_topics or any(ct.lower() in title.lower() for ct in consumed_topics):
                novelty = 0.35
            elif topic in frontier_topics or category in frontier_topics:
                novelty = 0.88
            else:
                novelty = 0.75

            # Difficulty Fit Score
            if item_difficulty_str == user_difficulty:
                diff_fit = 0.95
            elif (user_difficulty == "Beginner" and item_difficulty_str == "Advanced"):
                diff_fit = 0.40
            else:
                diff_fit = 0.75

            learning_pot = round(float(item.get("learningPotential", 0.85)) * diff_fit, 2)
            gen_conf = round(min(0.95, max(0.60, (novelty * 0.4 + diff_fit * 0.6))), 2)

            # Classify into candidateType
            if any(t in primary_set for t in item_tags):
                cand_type = CandidateType.FAMILIAR
                match_score = 0.92
            elif any(t in secondary_set or t in frontier_set for t in item_tags):
                cand_type = CandidateType.ADJACENT
                match_score = 0.85
            else:
                cand_type = CandidateType.EXPLORATORY
                match_score = 0.65

            candidate = CandidateItem(
                candidateId=f"CAND_{item.get('contentId', '000')}",
                title=title,
                topic=topic,
                category=category,
                candidateType=cand_type,
                description=item.get("description", ""),
                source="demo",
                interestPath=interest_path,
                interestMatch=match_score,
                novelty=novelty,
                learningPotential=learning_pot,
                difficulty=item_difficulty_str,
                generationConfidence=gen_conf
            )

            if cand_type == CandidateType.FAMILIAR:
                familiar_candidates.append(candidate)
            elif cand_type == CandidateType.ADJACENT:
                adjacent_candidates.append(candidate)
            else:
                exploratory_candidates.append(candidate)

        # 3. Balance Candidate Pool Diversity (30-40% Familiar, 40-50% Adjacent, 10-30% Exploratory)
        familiar_candidates.sort(key=lambda x: x.learningPotential, reverse=True)
        adjacent_candidates.sort(key=lambda x: x.learningPotential, reverse=True)
        exploratory_candidates.sort(key=lambda x: x.learningPotential, reverse=True)

        target_fam = max(2, int(self.target_candidate_count * 0.35))
        target_adj = max(3, int(self.target_candidate_count * 0.45))
        target_exp = max(1, self.target_candidate_count - target_fam - target_adj)

        selected_pool: List[CandidateItem] = []
        selected_pool.extend(familiar_candidates[:target_fam])
        selected_pool.extend(adjacent_candidates[:target_adj])
        selected_pool.extend(exploratory_candidates[:target_exp])

        # Fill remaining slots up to target_candidate_count if needed
        all_remaining = [
            c for c in familiar_candidates[target_fam:] + adjacent_candidates[target_adj:] + exploratory_candidates[target_exp:]
            if c not in selected_pool
        ]
        needed = self.target_candidate_count - len(selected_pool)
        if needed > 0 and all_remaining:
            selected_pool.extend(all_remaining[:needed])

        duration_ms = int((time.time() - start_time) * 1000)
        logger.info(
            f"CandidateGenerationAgent generated {len(selected_pool)} candidates for {user_id} in {duration_ms}ms "
            f"(Familiar={len([c for c in selected_pool if c.candidateType == CandidateType.FAMILIAR])}, "
            f"Adjacent={len([c for c in selected_pool if c.candidateType == CandidateType.ADJACENT])}, "
            f"Exploratory={len([c for c in selected_pool if c.candidateType == CandidateType.EXPLORATORY])})"
        )

        return CandidateGenerationResponse(
            success=True,
            candidateCount=len(selected_pool),
            candidates=selected_pool
        )
