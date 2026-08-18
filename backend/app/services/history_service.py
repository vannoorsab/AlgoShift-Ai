from typing import List, Dict, Any, Optional
from app.models.history import HistoryEvent, Analytics, KpiSummary, AgentPipeline
from app.models.user import UserSettings
from app.repositories.interest_repository import InterestRepository
from app.repositories.agent_run_repository import AgentRunRepository
from app.repositories.user_repository import UserRepository
from app.orchestration.pipeline import AgentOrchestrator
from app.services.seed_service import INITIAL_HISTORY

class HistoryService:
    def __init__(self, repo: Optional[InterestRepository] = None):
        self.repo = repo or InterestRepository()

    async def get_history(self, user_id: str) -> List[HistoryEvent]:
        # Return mock / stored history timeline
        return [HistoryEvent(**h) for h in INITIAL_HISTORY]

class AnalyticsService:
    async def get_analytics(self, user_id: str) -> Analytics:
        return Analytics(
            kpis=KpiSummary(
                recommendationsGenerated=248,
                recommendationsAccepted=173,
                usefulContentPct=82,
                hypeContentRejected=41,
                topInterest="Software Engineering"
            ),
            interestEvolution=[
                {"date": "Wk 1", "Software Engineering": 60, "Cloud": 20, "AI": 15, "Gaming": 55},
                {"date": "Wk 2", "Software Engineering": 68, "Cloud": 28, "AI": 22, "Gaming": 48},
                {"date": "Wk 3", "Software Engineering": 74, "Cloud": 35, "AI": 30, "Gaming": 40},
                {"date": "Wk 4", "Software Engineering": 81, "Cloud": 44, "AI": 38, "Gaming": 33},
                {"date": "Wk 5", "Software Engineering": 87, "Cloud": 53, "AI": 48, "Gaming": 28},
                {"date": "Wk 6", "Software Engineering": 92, "Cloud": 61, "AI": 57, "Gaming": 24}
            ],
            recommendationAcceptance=[
                {"label": "Wk 1", "accepted": 12, "rejected": 6},
                {"label": "Wk 2", "accepted": 18, "rejected": 5},
                {"label": "Wk 3", "accepted": 24, "rejected": 7},
                {"label": "Wk 4", "accepted": 31, "rejected": 8},
                {"label": "Wk 5", "accepted": 38, "rejected": 6},
                {"label": "Wk 6", "accepted": 50, "rejected": 9}
            ],
            categoryDistribution=[
                {"category": "Backend", "value": 28},
                {"category": "DSA", "value": 22},
                {"category": "AI", "value": 16},
                {"category": "Cloud", "value": 14},
                {"category": "Java", "value": 12},
                {"category": "Security", "value": 8}
            ],
            educationalValue=[
                {"label": "Wk 1", "value": 62},
                {"label": "Wk 2", "value": 68},
                {"label": "Wk 3", "value": 71},
                {"label": "Wk 4", "value": 78},
                {"label": "Wk 5", "value": 83},
                {"label": "Wk 6", "value": 88}
            ],
            hypeRejectionRate=[
                {"label": "Wk 1", "rejected": 4, "approved": 14},
                {"label": "Wk 2", "rejected": 5, "approved": 18},
                {"label": "Wk 3", "rejected": 7, "approved": 24},
                {"label": "Wk 4", "rejected": 8, "approved": 31},
                {"label": "Wk 5", "rejected": 6, "approved": 38},
                {"label": "Wk 6", "rejected": 9, "approved": 50}
            ],
            difficultyDistribution=[
                {"difficulty": "Beginner", "value": 34},
                {"difficulty": "Intermediate", "value": 48},
                {"difficulty": "Advanced", "value": 18}
            ]
        )

class AgentService:
    def __init__(self, repo: Optional[AgentRunRepository] = None):
        self.repo = repo or AgentRunRepository()
        self.orchestrator = AgentOrchestrator()

    async def get_agent_runs(self, user_id: str) -> AgentPipeline:
        run = await self.repo.get_latest_by_user(user_id)
        if run:
            return AgentPipeline(**run)
        return await self.orchestrator.execute_pipeline(user_id, {})

class UserService:
    def __init__(self, repo: Optional[UserRepository] = None):
        self.repo = repo or UserRepository()

    async def get_settings(self, user_id: str) -> UserSettings:
        st = await self.repo.get_settings(user_id)
        if st:
            return UserSettings(**st)
        return UserSettings(
            preferredDifficulty="Intermediate",
            contentPreferences=["AI", "DSA", "Java", "Cloud", "Career"],
            recommendationControls={
                "moreEducational": 70,
                "moreCareerFocused": 60,
                "moreTechnical": 55,
                "moreDiverse": 45
            },
            hypeSensitivity=80
        )

    async def update_settings(self, user_id: str, settings: UserSettings) -> UserSettings:
        await self.repo.update_settings(user_id, settings.model_dump())
        return settings
