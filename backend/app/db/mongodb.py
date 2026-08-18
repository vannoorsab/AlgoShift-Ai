import asyncio
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config.settings import settings
from app.core.logging import logger

class DatabaseManager:
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None

db_manager = DatabaseManager()

# Collection names constants
COLLECTION_USERS = "users"
COLLECTION_REELS = "reels"
COLLECTION_INTERACTIONS = "interactions"
COLLECTION_INTEREST_PROFILES = "interest_profiles"
COLLECTION_INTEREST_HISTORY = "interest_history"
COLLECTION_INTEREST_GRAPH = "interest_graph"
COLLECTION_RECOMMENDATIONS = "recommendations"
COLLECTION_RECOMMENDATION_CATALOG = "recommendation_catalog"
COLLECTION_FEEDBACK = "feedback"
COLLECTION_AGENT_RUNS = "agent_runs"
COLLECTION_WORKFLOW_RUNS = "workflow_runs"

ALL_COLLECTIONS = [
    COLLECTION_USERS,
    COLLECTION_REELS,
    COLLECTION_INTERACTIONS,
    COLLECTION_INTEREST_PROFILES,
    COLLECTION_INTEREST_HISTORY,
    COLLECTION_INTEREST_GRAPH,
    COLLECTION_RECOMMENDATIONS,
    COLLECTION_RECOMMENDATION_CATALOG,
    COLLECTION_FEEDBACK,
    COLLECTION_AGENT_RUNS,
    COLLECTION_WORKFLOW_RUNS,
]

async def connect_to_mongo(custom_client: Optional[AsyncIOMotorClient] = None):
    logger.info("Initializing MongoDB client...")
    if custom_client is not None:
        db_manager.client = custom_client
    else:
        db_manager.client = AsyncIOMotorClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=3000
        )
    db_manager.db = db_manager.client[settings.MONGODB_DB_NAME]
    
    try:
        await db_manager.client.admin.command('ping')
        logger.info(f"Successfully connected to MongoDB at {settings.MONGODB_URI}")
    except Exception as e:
        logger.warning(f"MongoDB ping warning/failure (backend running in fallback mode): {e}")

    await create_indexes()

async def close_mongo_connection():
    if db_manager.client:
        logger.info("Closing MongoDB connection...")
        db_manager.client.close()
        logger.info("MongoDB connection closed.")

async def create_indexes():
    if db_manager.db is None:
        return
    try:
        # Create indexes for collections
        await db_manager.db[COLLECTION_USERS].create_index("id", unique=True)
        await db_manager.db[COLLECTION_REELS].create_index("id", unique=True)
        await db_manager.db[COLLECTION_INTERACTIONS].create_index([("reelId", 1), ("timestamp", -1)])
        await db_manager.db[COLLECTION_INTEREST_PROFILES].create_index("userId")
        await db_manager.db[COLLECTION_INTEREST_GRAPH].create_index("userId", unique=True)
        await db_manager.db[COLLECTION_RECOMMENDATIONS].create_index("userId")
        await db_manager.db[COLLECTION_RECOMMENDATION_CATALOG].create_index("contentId", unique=True)
        await db_manager.db[COLLECTION_FEEDBACK].create_index("recommendationId")
        await db_manager.db[COLLECTION_AGENT_RUNS].create_index("userId")
        await db_manager.db[COLLECTION_WORKFLOW_RUNS].create_index("runId", unique=True)
        await db_manager.db[COLLECTION_WORKFLOW_RUNS].create_index("userId")
        logger.info("MongoDB index creation complete.")
    except Exception as e:
        logger.warning(f"Index creation warning: {e}")

def get_database() -> AsyncIOMotorDatabase:
    if db_manager.db is None:
        raise RuntimeError("Database is not initialized. Call connect_to_mongo first.")
    return db_manager.db
