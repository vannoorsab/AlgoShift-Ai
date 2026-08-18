from typing import Dict, Any

class ScoringEngine:
    """Scoring engine contract for calculating educational vs hype scores."""
    
    @staticmethod
    def calculate_relevance(interest_score: int, novelty_score: int) -> int:
        return min(100, max(0, int(interest_score * 0.7 + novelty_score * 0.3)))
