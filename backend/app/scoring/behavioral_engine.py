import math
import datetime
from typing import Dict, Any, Tuple

class BehavioralScoringEngine:
    """
    Deterministic behavioral scoring engine for AlgoShift AI.
    Calculates interaction weights and recency decay without LLM arithmetic.
    """
    def __init__(self, lambda_decay: float = 0.1):
        self.lambda_decay = lambda_decay

    def calculate_interaction_weight(self, interaction: Dict[str, Any]) -> Tuple[float, float]:
        """
        Returns (base_score, active_engagement_score).
        """
        watch_pct = float(interaction.get("watchPercentage", 0))
        action = str(interaction.get("action", "")).lower()
        liked = bool(interaction.get("liked", False))
        saved = bool(interaction.get("saved", False))
        shared = bool(interaction.get("shared", False))
        rewatched = bool(interaction.get("rewatched", False)) or action == "replay"

        # 1. Base watch score
        if action == "skip" or watch_pct < 25.0:
            if action == "skip" and watch_pct <= 25.0:
                base_score = -1.0
            else:
                base_score = -0.5
        elif 25.0 <= watch_pct < 50.0:
            base_score = 0.0
        elif 50.0 <= watch_pct < 80.0:
            base_score = 0.5
        else: # watch_pct >= 80.0
            base_score = 1.0

        # 2. Active engagement bonuses
        active_score = 0.0
        if rewatched:
            active_score += 1.5
        if liked or action == "like":
            active_score += 2.0
        if saved or action == "save":
            active_score += 3.0
        if shared or action == "share":
            active_score += 3.0

        return base_score, active_score

    def calculate_recency_weight(self, timestamp_str: str, current_time: datetime.datetime = None) -> float:
        """
        Exponential decay: w(t) = e^(-lambda * delta_days)
        """
        if current_time is None:
            current_time = datetime.datetime.utcnow()

        try:
            # Parse ISO format timestamp
            ts_clean = timestamp_str.replace("Z", "+00:00")
            dt = datetime.datetime.fromisoformat(ts_clean)
            if dt.tzinfo is not None:
                current_time = current_time.replace(tzinfo=dt.tzinfo)
            delta_days = max(0.0, (current_time - dt).total_seconds() / 86400.0)
        except Exception:
            delta_days = 0.0

        return math.exp(-self.lambda_decay * delta_days)

    def calculate_interaction_score(self, interaction: Dict[str, Any], current_time: datetime.datetime = None) -> Dict[str, float]:
        base_score, active_score = self.calculate_interaction_weight(interaction)
        recency = self.calculate_recency_weight(interaction.get("timestamp", ""), current_time)
        
        total_raw = base_score + active_score
        weighted_score = total_raw * recency

        return {
            "base_score": base_score,
            "active_score": active_score,
            "total_raw": total_raw,
            "recency_weight": recency,
            "weighted_score": weighted_score
        }
