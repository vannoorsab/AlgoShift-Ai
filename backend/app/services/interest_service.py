import time
import datetime
from typing import List, Dict, Any, Optional
from app.repositories.interest_repository import InterestRepository
from app.repositories.interaction_repository import InteractionRepository
from app.repositories.reel_repository import ReelRepository
from app.repositories.agent_run_repository import AgentRunRepository
from app.agents.interest_inference import InterestInferenceAgent
from app.models.interest import (
    Interest, InterestInference, InterestGraph, InterestGraphNode,
    InterestGraphEdge, InterestProfile, InterestItem
)
from app.services.seed_service import INITIAL_INTERESTS, INITIAL_GRAPH

class InterestService:
    def __init__(
        self,
        interest_repo: Optional[InterestRepository] = None,
        interaction_repo: Optional[InteractionRepository] = None,
        reel_repo: Optional[ReelRepository] = None,
        agent_repo: Optional[AgentRunRepository] = None
    ):
        self.repo = interest_repo or InterestRepository()
        self.interaction_repo = interaction_repo or InteractionRepository()
        self.reel_repo = reel_repo or ReelRepository()
        self.agent_repo = agent_repo or AgentRunRepository()
        self.agent = InterestInferenceAgent()

    async def infer_interests(self, user_id: str) -> InterestProfile:
        start_time = time.time()
        now = datetime.datetime.utcnow().isoformat() + "Z"
        
        # 1. Fetch user interactions
        interactions = await self.interaction_repo.get_by_user(user_id, limit=100)
        
        # 2. Build map of Reel ID -> Analysis document from MongoDB reels collection
        reel_docs = await self.reel_repo.find_many({})
        reel_analyses: Dict[str, Dict[str, Any]] = {}
        for r in reel_docs:
            reel_id = r.get("reelId")
            if reel_id and "analysis" in r:
                reel_analyses[reel_id] = r["analysis"]
                # Include title if stored inside content
                if "content" in r and "title" in r["content"]:
                    reel_analyses[reel_id]["title"] = r["content"]["title"]
        
        # If any reel from interaction is not in DB, populate from demo dataset
        from app.services.demo_dataset import DEMO_REELS
        from app.agents.reel_understanding import ReelUnderstandingAgent
        understanding_agent = ReelUnderstandingAgent()
        
        for inter in interactions:
            r_id = inter.get("reelId")
            if r_id and r_id not in reel_analyses:
                if r_id in DEMO_REELS:
                    demo_content = DEMO_REELS[r_id]
                    analysis_res = await understanding_agent.analyze(demo_content)
                    analysis_dict = analysis_res.model_dump()
                    analysis_dict["title"] = demo_content.title
                    reel_analyses[r_id] = analysis_dict

        # 3. Execute InterestInferenceAgent
        try:
            profile: InterestProfile = await self.agent.infer(user_id, interactions, reel_analyses)
            duration_ms = int((time.time() - start_time) * 1000)
            
            # 4. Save profile into MongoDB interest_profiles & interest_history
            await self.repo.save_profile(profile.model_dump())
            
            # 5. Log agent run to agent_runs
            agent_run_doc = {
                "agentName": self.agent.agent_name,
                "agentVersion": self.agent.agent_version,
                "userId": user_id,
                "inputInteractionCount": len(interactions),
                "status": "success",
                "durationMs": duration_ms,
                "overallConfidence": profile.overallConfidence,
                "createdAt": now
            }
            await self.agent_repo.insert_one(agent_run_doc)
            
            return profile
            
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            error_run_doc = {
                "agentName": self.agent.agent_name,
                "agentVersion": self.agent.agent_version,
                "userId": user_id,
                "inputInteractionCount": len(interactions),
                "status": "failure",
                "error": str(e),
                "durationMs": duration_ms,
                "createdAt": now
            }
            await self.agent_repo.insert_one(error_run_doc)
            raise e

    async def get_user_interests(self, user_id: str) -> List[Interest]:
        docs = await self.repo.get_interests(user_id)
        if docs:
            return [Interest(**d) for d in docs]
        return [Interest(**d) for d in INITIAL_INTERESTS]

    async def get_user_inference(self, user_id: str) -> InterestInference:
        inf = await self.repo.get_inference(user_id)
        if inf:
            return InterestInference(**inf)
        return InterestInference(
            primaryInterest="Software Engineering",
            supportingSignals=["Java", "Coding Interviews", "Software Engineer Lifestyle", "Developer Hardware"],
            note="AI inferred a broader interest instead of relying on a single topic."
        )

    async def get_user_graph(self, user_id: str) -> InterestGraph:
        doc = await self.repo.get_graph(user_id)
        if doc:
            nodes = [InterestGraphNode(**n) for n in doc.get("nodes", [])]
            edges = [InterestGraphEdge(**{"from": e.get("from", e.get("from_node")), "to": e["to"]}) for e in doc.get("edges", [])]
            return InterestGraph(root=doc.get("root", "Technology"), nodes=nodes, edges=edges)
        
        nodes = [InterestGraphNode(**n) for n in INITIAL_GRAPH["nodes"]]
        edges = [InterestGraphEdge(**{"from": e["from"], "to": e["to"]}) for e in INITIAL_GRAPH["edges"]]
        return InterestGraph(root=INITIAL_GRAPH["root"], nodes=nodes, edges=edges)

    async def get_user_timeline(self, user_id: str) -> List[Dict[str, Any]]:
        docs = await self.repo.get_timeline(user_id)
        if docs:
            return docs
        return [
            {"date": "Wk 1", "Software Engineering": 60, "Cloud": 20, "AI": 15, "Gaming": 55},
            {"date": "Wk 2", "Software Engineering": 68, "Cloud": 28, "AI": 22, "Gaming": 48},
            {"date": "Wk 3", "Software Engineering": 74, "Cloud": 35, "AI": 30, "Gaming": 40},
            {"date": "Wk 4", "Software Engineering": 81, "Cloud": 44, "AI": 38, "Gaming": 33},
            {"date": "Wk 5", "Software Engineering": 87, "Cloud": 53, "AI": 48, "Gaming": 28},
            {"date": "Wk 6", "Software Engineering": 92, "Cloud": 61, "AI": 57, "Gaming": 24}
        ]
