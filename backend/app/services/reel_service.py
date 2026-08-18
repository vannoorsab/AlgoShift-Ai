import time
import datetime
from typing import Dict, Any, Optional
from app.repositories.reel_repository import ReelRepository
from app.repositories.agent_run_repository import AgentRunRepository
from app.services.ingestion.service import ReelIngestionService
from app.agents.reel_understanding import ReelUnderstandingAgent
from app.models.reel import ReelContent, ReelAnalysis, AnalyzeReelResponse

class ReelService:
    def __init__(
        self,
        reel_repo: Optional[ReelRepository] = None,
        agent_repo: Optional[AgentRunRepository] = None
    ):
        self.reel_repo = reel_repo or ReelRepository()
        self.agent_repo = agent_repo or AgentRunRepository()
        self.ingestion_service = ReelIngestionService()
        self.agent = ReelUnderstandingAgent()

    async def analyze_reel(self, input_data: Dict[str, Any]) -> AnalyzeReelResponse:
        start_time = time.time()
        now = datetime.datetime.utcnow().isoformat() + "Z"
        
        # 1. Ingest content into normalized ReelContent
        content: ReelContent = await self.ingestion_service.ingest(input_data)
        
        try:
            # 2. Run ReelUnderstandingAgent
            analysis: ReelAnalysis = await self.agent.analyze(content)
            duration_ms = int((time.time() - start_time) * 1000)
            
            # 3. Save analysis and record to MongoDB reels collection
            await self.reel_repo.save_reel_record(content, analysis)
            
            # 4. Log agent execution to agent_runs collection
            agent_run_doc = {
                "agentName": self.agent.agent_name,
                "agentVersion": self.agent.agent_version,
                "reelId": content.reelId,
                "status": "success",
                "confidence": analysis.confidence,
                "durationMs": duration_ms,
                "createdAt": now
            }
            await self.agent_repo.insert_one(agent_run_doc)
            
            return AnalyzeReelResponse(success=True, analysis=analysis)
            
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            # Log failure to agent_runs collection
            error_run_doc = {
                "agentName": self.agent.agent_name,
                "agentVersion": self.agent.agent_version,
                "reelId": content.reelId if content else input_data.get("reelId", "UNKNOWN"),
                "status": "failure",
                "error": str(e),
                "durationMs": duration_ms,
                "createdAt": now
            }
            await self.agent_repo.insert_one(error_run_doc)
            raise e

    async def get_reel_by_id(self, reel_id: str) -> Optional[Dict[str, Any]]:
        return await self.reel_repo.get_by_id(reel_id)
