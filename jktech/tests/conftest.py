import asyncio
import pytest
import pytest_asyncio
from typing import AsyncGenerator, Generator
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.db.base import Base, get_async_session
from app.main import app
from app.core.config import settings
from app.services.user_service import UserService

# Use an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=NullPool,
)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

app.dependency_overrides[get_async_session] = override_get_async_session

@pytest_asyncio.fixture
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

@pytest_asyncio.fixture
async def client() -> AsyncGenerator[TestClient, None]:
    with TestClient(app) as c:
        yield c

@pytest_asyncio.fixture
async def init_db() -> AsyncGenerator[None, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def test_user(async_session: AsyncSession) -> dict:
    """Create a test user and return its data."""
    user_service = UserService()
    user = await user_service.create_user(
        session=async_session,
        username="testuser",
        email="test@example.com",
        password="password123",
        is_superuser=False
    )
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "password": "password123"  # Store the plain password for testing
    }

@pytest_asyncio.fixture
async def test_superuser(async_session: AsyncSession) -> dict:
    """Create a test superuser and return its data."""
    user_service = UserService()
    user = await user_service.create_user(
        session=async_session,
        username="admin",
        email="admin@example.com",
        password="adminpass123",
        is_superuser=True
    )
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "password": "adminpass123"  # Store the plain password for testing
    }
