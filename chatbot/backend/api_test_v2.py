import requests
import pytest
import time

BASE_URL = "http://localhost:8000"

def get_unique_username():
    return f"testuser_{int(time.time())}"

def test_root_endpoint():
    """Verify API root endpoint is accessible"""
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert "endpoints" in response.json()

def test_user_workflow():
    """Test complete user registration and authentication flow"""
    # Create unique test user
    user_data = {
        "username": get_unique_username(),
        "email": f"{get_unique_username()}@example.com",
        "password": "testpassword123"
    }
    
    # Test user creation
    create_res = requests.post(f"{BASE_URL}/users/", json=user_data)
    assert create_res.status_code == 200
    
    # Test authentication
    auth_res = requests.post(
        f"{BASE_URL}/token",
        data={
            "username": user_data["username"],
            "password": user_data["password"]
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert auth_res.status_code == 200
    token = auth_res.json().get("access_token")
    assert token is not None
    
    # Test protected endpoint
    users_res = requests.get(
        f"{BASE_URL}/users/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert users_res.status_code == 200
    assert isinstance(users_res.json(), list)