import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.asyncio

async def test_login(client: TestClient, init_db, test_user: dict):
    """Test user login."""
    response = client.post(
        "/api/auth/login",
        data={
            "username": test_user["username"],
            "password": test_user["password"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

async def test_login_wrong_password(client: TestClient, init_db, test_user: dict):
    """Test login with wrong password."""
    response = client.post(
        "/api/auth/login",
        data={
            "username": test_user["username"],
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]

async def test_login_nonexistent_user(client: TestClient, init_db):
    """Test login with nonexistent user."""
    response = client.post(
        "/api/auth/login",
        data={
            "username": "nonexistentuser",
            "password": "password123"
        }
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]
