import time
import datetime
import uuid
import asyncio
from typing import List, Dict, Any, Optional
from app.models.workflow import (
    AnalyzeRequest, AnalyzeResponse, AnalyzeNextRequest, WorkflowStepStatus, WorkflowError
)
from app.models.explanation import ExplainRecommendationResponse
from app.core.errors import ValidationException, EntityNotFoundException, DatabaseException
from app.services.ingestion.service import ReelIngestionService
from app.services.recommendation_service import RecommendationService
from app.agents.reel_understanding import ReelUnderstandingAgent
from app.agents.interest_inference import InterestInferenceAgent
from app.db.mongodb import db_manager, COLLECTION_WORKFLOW_RUNS
from app.core.logging import logger

class WorkflowOrchestratorService:
    """
    Central Workflow Orchestrator connecting Agents 1–6 into a reliable,
    end-to-end recommendation pipeline with explicit domain error handling.
    """

    def __init__(self):
        self.ingestion_service = ReelIngestionService()
        self.recommendation_service = RecommendationService()
        self.reel_agent = ReelUnderstandingAgent()
        self.interest_agent = InterestInferenceAgent()

    async def run_pipeline(
        self,
        request: AnalyzeRequest,
        upload_file: Optional[Any] = None
    ) -> AnalyzeResponse:
        start_time = time.time()
        now = datetime.datetime.utcnow().isoformat() + "Z"
        run_id = f"RUN_{uuid.uuid4().hex[:8]}"

        user_id = request.userId
        input_mode = request.inputMode

        steps: List[WorkflowStepStatus] = []
        current_status = "queued"

        # Initialize workflow run in MongoDB
        initial_run_doc = {
            "runId": run_id,
            "userId": user_id,
            "inputMode": input_mode,
            "status": current_status,
            "steps": [],
            "startedAt": now
        }
        await db_manager.db[COLLECTION_WORKFLOW_RUNS].insert_one(initial_run_doc)

        async def update_step(step_name: str, agent_name: str, fn, retry_count=2):
            nonlocal current_status
            current_status = step_name
            await db_manager.db[COLLECTION_WORKFLOW_RUNS].update_one(
                {"runId": run_id},
                {"$set": {"status": current_status}}
            )

            step_start = time.time()
            attempts = 0
            while attempts <= retry_count:
                try:
                    res = await asyncio.wait_for(fn(), timeout=15.0)
                    step_duration = int((time.time() - step_start) * 1000)
                    steps.append(WorkflowStepStatus(agent=agent_name, status="completed", durationMs=step_duration))
                    return res
                except ValidationException as val_err:
                    step_duration = int((time.time() - step_start) * 1000)
                    steps.append(WorkflowStepStatus(agent=agent_name, status="failed", durationMs=step_duration, error=val_err.message))
                    raise val_err
                except (EntityNotFoundException, DatabaseException) as domain_err:
                    step_duration = int((time.time() - step_start) * 1000)
                    steps.append(WorkflowStepStatus(agent=agent_name, status="failed", durationMs=step_duration, error=domain_err.message))
                    raise domain_err
                except Exception as e:
                    attempts += 1
                    e_type = type(e).__name__
                    if attempts > retry_count or "REEL_ACCESS_ERROR" in str(e):
                        step_duration = int((time.time() - step_start) * 1000)
                        steps.append(WorkflowStepStatus(agent=agent_name, status="failed", durationMs=step_duration, error=str(e)))
                        raise e
                    await asyncio.sleep(0.2)

        try:
            # 1. INGESTION STEP
            current_reel_id = "R003"
            
            async def step_ingest():
                nonlocal current_reel_id
                if input_mode == "upload" and upload_file:
                    file_bytes = await upload_file.read() if hasattr(upload_file, "read") else upload_file
                    filename = getattr(upload_file, "filename", "uploaded_reel.mp4")
                    norm = await self.ingestion_service.ingest_upload(file_bytes, filename)
                    current_reel_id = norm.reelId
                elif input_mode == "url" and request.url:
                    norm = await self.ingestion_service.ingest_url(request.url)
                    current_reel_id = norm.reelId
                else:
                    norms = await self.ingestion_service.ingest_dataset()
                    if user_id == "student_002":
                        current_reel_id = "R007"
                    elif user_id == "student_003":
                        current_reel_id = "R006"
                    elif user_id == "student_004":
                        current_reel_id = "R008"
                    else:
                        current_reel_id = request.reelId or "R003"
                return current_reel_id

            await update_step("ingesting", "ReelIngestionLayer", step_ingest)

            # 2. AGENT 1 STEP — Reel Understanding (Idempotent cache check)
            async def step_agent1():
                cached = await db_manager.db["reels"].find_one({"id": current_reel_id})
                if cached and cached.get("analysis"):
                    return cached
                return await self.reel_agent.analyze_reel(current_reel_id)

            await update_step("understanding", "ReelUnderstandingAgent", step_agent1)

            # 3. AGENT 2 STEP — Interest Inference
            async def step_agent2():
                return await self.interest_agent.infer_interests(user_id)

            profile = await update_step("inferring_interests", "InterestInferenceAgent", step_agent2)

            # 4. AGENT 3 STEP — Candidate Generation
            async def step_agent3():
                return await self.recommendation_service.generate_candidate_pool(user_id)

            gen_res = await update_step("generating_candidates", "CandidateGenerationAgent", step_agent3)

            # 5. AGENT 4 STEP — Quality / Hype Shield (Typed model data flow)
            candidates_dict = [c.model_dump() for c in gen_res.candidates]
            
            async def step_agent4():
                return await self.recommendation_service.quality_agent.evaluate_batch(user_id, candidates_dict)

            qual_res = await update_step("evaluating_quality", "ContentQualityAgent", step_agent4)

            # 6. AGENT 5 STEP — Ranking Engine
            async def step_agent5():
                return await self.recommendation_service.ranking_agent.rank(
                    user_id=user_id,
                    current_reel_id=current_reel_id,
                    candidates=candidates_dict,
                    quality_evaluations=qual_res.evaluations,
                    interest_profile=profile
                )

            rank_res = await update_step("ranking", "RecommendationRankingEngine", step_agent5)

            # 7. AGENT 6 STEP — Explanation & 8-Field Output
            current_reel_dict = {"reelId": current_reel_id, "title": "Coding Interview Joke"}
            if current_reel_id.startswith("R0"):
                from app.services.demo_dataset import DEMO_REELS
                if current_reel_id in DEMO_REELS:
                    current_reel_dict = {"reelId": current_reel_id, "title": DEMO_REELS[current_reel_id].title}

            async def step_agent6():
                return await self.recommendation_service.explanation_agent.explain(
                    user_id=user_id,
                    current_reel=current_reel_dict,
                    interest_profile=profile,
                    ranking_response=rank_res,
                    quality_evaluations=qual_res
                )

            explain_res: ExplainRecommendationResponse = await update_step("explaining", "ExplanationAgent", step_agent6)

            completion_time = datetime.datetime.utcnow().isoformat() + "Z"
            workflow_summary = {"status": "completed", "stepsCompleted": len(steps)}

            await db_manager.db[COLLECTION_WORKFLOW_RUNS].update_one(
                {"runId": run_id},
                {
                    "$set": {
                        "status": "completed",
                        "steps": [s.model_dump() for s in steps],
                        "result": explain_res.result.model_dump(),
                        "completedAt": completion_time
                    }
                }
            )

            return AnalyzeResponse(
                success=True,
                runId=run_id,
                result=explain_res.result,
                evidence=explain_res.evidence,
                workflow=workflow_summary
            )

        except ValidationException as val_exc:
            logger.warning(f"WorkflowOrchestrator pipeline validation error at '{current_status}': {val_exc.message}")
            completion_time = datetime.datetime.utcnow().isoformat() + "Z"
            await db_manager.db[COLLECTION_WORKFLOW_RUNS].update_one(
                {"runId": run_id},
                {
                    "$set": {
                        "status": "failed",
                        "failedStep": current_status,
                        "steps": [s.model_dump() for s in steps],
                        "completedAt": completion_time
                    }
                }
            )
            return AnalyzeResponse(
                success=False,
                runId=run_id,
                workflow={"status": "failed", "failedStep": current_status},
                error=WorkflowError(step=current_status, code="REEL_ACCESS_ERROR", message=val_exc.message)
            )

        except (EntityNotFoundException, DatabaseException) as domain_exc:
            logger.error(f"WorkflowOrchestrator domain error at '{current_status}': {domain_exc.message}")
            completion_time = datetime.datetime.utcnow().isoformat() + "Z"
            await db_manager.db[COLLECTION_WORKFLOW_RUNS].update_one(
                {"runId": run_id},
                {"$set": {"status": "failed", "failedStep": current_status, "steps": [s.model_dump() for s in steps], "completedAt": completion_time}}
            )
            return AnalyzeResponse(
                success=False,
                runId=run_id,
                workflow={"status": "failed", "failedStep": current_status},
                error=WorkflowError(step=current_status, code="DOMAIN_ERROR", message=domain_exc.message)
            )

        except Exception as e:
            logger.error(f"WorkflowOrchestrator pipeline failed at step '{current_status}': {e}")
            error_msg = str(e)
            error_code = "PIPELINE_ERROR"
            if "URL" in error_msg or "retrieve Reel" in error_msg:
                error_code = "REEL_ACCESS_ERROR"

            completion_time = datetime.datetime.utcnow().isoformat() + "Z"
            await db_manager.db[COLLECTION_WORKFLOW_RUNS].update_one(
                {"runId": run_id},
                {
                    "$set": {
                        "status": "failed",
                        "failedStep": current_status,
                        "steps": [s.model_dump() for s in steps],
                        "completedAt": completion_time
                    }
                }
            )

            return AnalyzeResponse(
                success=False,
                runId=run_id,
                workflow={"status": "failed", "failedStep": current_status},
                error=WorkflowError(step=current_status, code=error_code, message=error_msg)
            )

    async def run_next_pipeline(self, user_id: str) -> AnalyzeResponse:
        req = AnalyzeRequest(userId=user_id, inputMode="dataset")
        return await self.run_pipeline(req)

    async def get_workflow_run(self, run_id: str) -> Optional[Dict[str, Any]]:
        return await db_manager.db[COLLECTION_WORKFLOW_RUNS].find_one({"runId": run_id})
