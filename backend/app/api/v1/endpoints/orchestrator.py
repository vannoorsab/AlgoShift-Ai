from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, status, Request, HTTPException
from app.models.workflow import AnalyzeRequest, AnalyzeResponse, AnalyzeNextRequest
from app.models.feedback import RecommendationFeedbackPayload, RecommendationFeedbackResponse
from app.services.workflow_orchestrator import WorkflowOrchestratorService
from app.services.recommendation_service import RecommendationService

router = APIRouter(tags=["Workflow Orchestrator"])

def get_orchestrator_service() -> WorkflowOrchestratorService:
    return WorkflowOrchestratorService()

def get_recommendation_service() -> RecommendationService:
    return RecommendationService()

@router.post("/analyze", response_model=AnalyzeResponse, status_code=status.HTTP_200_OK)
async def analyze_feed(
    request: Request,
    service: WorkflowOrchestratorService = Depends(get_orchestrator_service)
) -> AnalyzeResponse:
    """Main workflow endpoint orchestrating Agents 1–6 into a complete recommendation response."""
    content_type = request.headers.get("content-type", "").lower()
    
    u_id = "student_001"
    mode = "dataset"
    u_url = None
    upload_file = None

    if "multipart/form-data" in content_type or "application/x-www-form-urlencoded" in content_type:
        form = await request.form()
        u_id = str(form.get("userId") or "student_001")
        mode = str(form.get("inputMode") or "dataset")
        u_url = str(form.get("url")) if form.get("url") else None
        file_obj = form.get("file")
        if file_obj and hasattr(file_obj, "filename"):
            upload_file = file_obj
    else:
        try:
            body = await request.json()
            if isinstance(body, dict):
                u_id = body.get("userId", "student_001")
                mode = body.get("inputMode", "dataset")
                u_url = body.get("url")
        except Exception:
            pass

    req = AnalyzeRequest(userId=u_id, inputMode=mode, url=u_url)
    return await service.run_pipeline(req, upload_file=upload_file)

@router.post("/analyze/next", response_model=AnalyzeResponse, status_code=status.HTTP_200_OK)
async def analyze_next(
    payload: AnalyzeNextRequest,
    service: WorkflowOrchestratorService = Depends(get_orchestrator_service)
) -> AnalyzeResponse:
    """Generates next recommendation post-feedback."""
    return await service.run_next_pipeline(payload.userId)

@router.post("/feedback", response_model=RecommendationFeedbackResponse, status_code=status.HTTP_200_OK)
async def process_feedback(
    payload: RecommendationFeedbackPayload,
    rec_service: RecommendationService = Depends(get_recommendation_service)
) -> RecommendationFeedbackResponse:
    """Alias endpoint for Agent 7 feedback processing."""
    return await rec_service.process_recommendation_feedback(payload)

@router.get("/workflows/{runId}", status_code=status.HTTP_200_OK)
async def get_workflow_run(
    runId: str,
    service: WorkflowOrchestratorService = Depends(get_orchestrator_service)
):
    """Retrieves status and timing metrics for a workflow run."""
    doc = await service.get_workflow_run(runId)
    if not doc:
        raise HTTPException(status_code=404, detail=f"Workflow run {runId} not found.")
    doc.pop("_id", None)
    return doc
