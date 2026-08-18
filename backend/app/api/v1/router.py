from fastapi import APIRouter
from app.api.v1.endpoints.reels import router as reels_router
from app.api.v1.endpoints.interactions import router as interactions_router
from app.api.v1.endpoints.interests import router as interests_router
from app.api.v1.endpoints.recommendations import router as recommendations_router
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.orchestrator import router as orchestrator_router

api_router = APIRouter()

api_router.include_router(reels_router)
api_router.include_router(interactions_router)
api_router.include_router(interests_router)
api_router.include_router(recommendations_router)
api_router.include_router(users_router)
api_router.include_router(orchestrator_router)
