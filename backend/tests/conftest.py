import pytest
import pytest_asyncio
from mongomock_motor import AsyncMongoMockClient
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db.mongodb import connect_to_mongo, close_mongo_connection, db_manager
from app.services.seed_service import seed_initial_data

@pytest_asyncio.fixture(scope="function", autouse=True)
async def mock_mongodb():
    # Setup in-memory mongomock_motor client
    mock_client = AsyncMongoMockClient()
    await connect_to_mongo(custom_client=mock_client)
    await seed_initial_data()
    yield
    await close_mongo_connection()

@pytest_asyncio.fixture(scope="function")
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
