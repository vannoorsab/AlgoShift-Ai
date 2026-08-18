from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.core.logging import logger
from app.core.errors import TechScrollBaseException, techscroll_exception_handler, generic_exception_handler
from app.db.mongodb import connect_to_mongo, close_mongo_connection, db_manager
from app.services.seed_service import seed_initial_data
from app.api.v1.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting TechScroll AI Backend ({settings.ENVIRONMENT})...")
    await connect_to_mongo()
    await seed_initial_data()
    yield
    logger.info("Shutting down TechScroll AI Backend...")
    await close_mongo_connection()

app = FastAPI(
    title="TechScroll AI API",
    description="Backend API for TechScroll AI — AI Agent Feed and Learning Recommendation System",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS Middleware (Allow all origins for public API access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(TechScrollBaseException, techscroll_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Health endpoint
@app.get("/health", status_code=status.HTTP_200_OK, tags=["Health"])
@app.get("/", status_code=status.HTTP_200_OK, tags=["Health"])
async def health_check():
    mongo_status = "connected" if db_manager.db is not None else "disconnected"
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "mongodb": mongo_status
    }

# Mount API routers (both /api and /api/v1 for 1:1 frontend parity)
app.include_router(api_router, prefix="/api")
app.include_router(api_router, prefix="/api/v1")
