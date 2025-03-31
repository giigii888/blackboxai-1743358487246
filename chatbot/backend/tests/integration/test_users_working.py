import pytest
from httpx import AsyncClient
from minimal_api_v4 import app

@pytest.mark.asyncio
async def test_get_users():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Get auth token
        auth_res = await client.post(
            "/token",
            data={"username": "testuser", "password": "testpassword"}
        )
        headers = {"Authorization": f"Bearer {auth_res.json()['access_token']}"}
        
        # Test endpoint
        response = await client.get("/users/", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json()["users"], list)

@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Get admin token
        admin_res = await client.post(
            "/token",
            data={"username": "admin", "password": "adminpassword"}
        )
        headers = {"Authorization": f"Bearer {admin_res.json()['access_token']}"}
        
        # Test creation
        test_user = {
            "username": "newtestuser",
            "email": "new@example.com",
            "password": "securepassword123"
        }
        response = await client.post("/users/", json=test_user, headers=headers)
        assert response.status_code == 200
        assert response.json()["message"] == "User created"