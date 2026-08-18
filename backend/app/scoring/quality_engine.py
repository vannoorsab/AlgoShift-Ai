import re
from typing import Dict, Any, Tuple, List
from app.models.quality import QualityAssessment, QualityDecision

HYPE_PATTERNS = [
    r"guarantee", r"guaranteed", r"100k", r"\$10,000", r"\$999", r"earn \$",
    r"get rich", r"secret trick", r"one skill", r"overnight", r"in 7 days",
    r"replace everyone", r"changes everything", r"get you a job"
]

PROMOTIONAL_PATTERNS = [
    r"buy my", r"masterclass", r"course", r"affiliate", r"sign up", r"discount", r"limited spot"
]

CLICKBAIT_PATTERNS = [
    r"10 ai tools", r"secret", r"shocking", r"never do this", r"stop doing", r"10x your", r"get you a job", r"earn \$"
]

class ContentQualityScoringEngine:
    """
    Deterministic scoring engine for ContentQualityAgent.
    Evaluates 10 quality dimensions and decision rules in Python without LLM arithmetic.
    """

    def analyze_patterns(self, text: str) -> Tuple[float, float, float, float]:
        text_lower = text.lower()
        
        hype_count = sum(1 for p in HYPE_PATTERNS if re.search(p, text_lower))
        promotional_count = sum(1 for p in PROMOTIONAL_PATTERNS if re.search(p, text_lower))
        clickbait_count = sum(1 for p in CLICKBAIT_PATTERNS if re.search(p, text_lower))

        hype_score = min(0.95, hype_count * 0.48)
        clickbait_score = min(0.95, clickbait_count * 0.45)
        promotional_score = min(0.95, promotional_count * 0.50)
        
        if hype_score >= 0.80:
            clickbait_score = max(clickbait_score, 0.88)
            misleading_risk = 0.90
        else:
            misleading_risk = min(0.95, (hype_score * 0.6 + clickbait_score * 0.4))

        return hype_score, clickbait_score, promotional_score, misleading_risk

    def calculate_quality(self, item: Dict[str, Any]) -> QualityAssessment:
        candidate_id = str(item.get("candidateId") or item.get("contentId") or "CAND_000")
        title = item.get("title", "")
        desc = item.get("description", "")
        combined_text = f"{title} {desc}"

        # Analyze Hype, Clickbait, Promotional, Misleading
        hype_score, clickbait_score, promo_score, misleading_risk = self.analyze_patterns(combined_text)

        # Content classification heuristics for educational, practical, depth, career, entertainment
        topic = item.get("topic", "").lower()
        category = item.get("category", "").lower()
        diff = item.get("difficulty", "Intermediate")

        # Developer meme detection (e.g. "When Your API Returns 500 in Production")
        is_meme = "500 in production" in combined_text.lower() or "meme" in combined_text.lower() or "humor" in combined_text.lower()
        
        if is_meme:
            educational_val = 0.60
            practical_val = 0.55
            tech_depth = 0.50
            career_rel = 0.50
            evidence_qual = 0.65
            entertainment_val = 0.95
            hype_score = min(hype_score, 0.20)
            clickbait_score = min(clickbait_score, 0.30)
            misleading_risk = min(misleading_risk, 0.15)
        elif hype_score > 0.80:
            educational_val = float(item.get("educationalValue", 0.30))
            practical_val = 0.28
            tech_depth = 0.25
            career_rel = 0.40
            evidence_qual = 0.30
            entertainment_val = 0.60
        else:
            educational_val = float(item.get("educationalValue", 0.88))
            practical_val = 0.90 if "api" in combined_text.lower() or "build" in combined_text.lower() or "index" in combined_text.lower() else 0.82
            tech_depth = 0.85 if diff == "Advanced" else 0.72
            career_rel = 0.75 if "interview" in combined_text.lower() or "career" in combined_text.lower() else 0.65
            evidence_qual = 0.80
            entertainment_val = 0.55

        # 1. Base Score calculation (weights sum to 100%)
        base_score = (
            educational_val * 0.30 +
            practical_val * 0.25 +
            tech_depth * 0.15 +
            career_rel * 0.10 +
            evidence_qual * 0.10 +
            entertainment_val * 0.05 +
            0.80 * 0.05  # Source Reliability
        )

        # 2. Penalties calculation
        hype_pen = hype_score * 0.35
        clickbait_pen = clickbait_score * 0.30
        misleading_pen = misleading_risk * 0.40
        promo_pen = promo_score * 0.20

        raw_quality = base_score - (hype_pen + clickbait_pen + misleading_pen + promo_pen)
        quality_score = round(max(0.0, min(1.0, raw_quality)), 2)

        # 3. Decision Logic Rules
        reasons = []
        if misleading_risk >= 0.85 or (hype_score >= 0.85 and educational_val < 0.50) or (clickbait_score >= 0.90 and practical_val < 0.45):
            decision = QualityDecision.REJECT
            if misleading_risk >= 0.85:
                reasons.append("High misleading claim risk and exaggerated promises")
            if hype_score >= 0.85:
                reasons.append("Excessive hype score with low technical depth")
            if promo_score >= 0.80:
                reasons.append("High promotional framing")
        elif hype_score >= 0.60 or promo_score >= 0.65 or educational_val < 0.55:
            decision = QualityDecision.PENALIZE
            if hype_score >= 0.60:
                reasons.append("Moderate hype penalty applied")
            if promo_score >= 0.65:
                reasons.append("Promotional framing detected")
            if educational_val < 0.55:
                reasons.append("Moderate educational value")
        else:
            decision = QualityDecision.ACCEPT
            reasons.append("Strong educational value")
            reasons.append("Substantive technical concept")
            reasons.append("Low hype")

        return QualityAssessment(
            candidateId=candidate_id,
            educationalValue=round(educational_val, 2),
            practicalUsefulness=round(practical_val, 2),
            technicalDepth=round(tech_depth, 2),
            careerRelevance=round(career_rel, 2),
            evidenceQuality=round(evidence_qual, 2),
            entertainmentValue=round(entertainment_val, 2),
            hypeScore=round(hype_score, 2),
            clickbaitScore=round(clickbait_score, 2),
            promotionalScore=round(promo_score, 2),
            misleadingClaimRisk=round(misleading_risk, 2),
            qualityScore=quality_score,
            decision=decision,
            reasons=reasons
        )
