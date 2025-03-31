import pytest
from fastapi.testclient import TestClient
from minimal_api_v4 import app

@pytest.fixture
def client():
    return TestClient(app)

def test_get_users(client):
    # Get auth token
    auth_res = client.post(
        "/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    headers = {"Authorization": f"Bearer {auth_res.json()['access_token']}"}
    
    # Test endpoint
    response = client.get("/users/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json()["users"], list)

def test_create_user(client):
    # Get admin token
    admin_res = client.post(
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
    response = client.post("/users/", json=test_user, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "User created"