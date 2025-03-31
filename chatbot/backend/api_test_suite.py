import requests
import pytest

BASE_URL = "http://localhost:8000"

def test_root_endpoint():
    """Test API root endpoint returns 200 OK with endpoints list"""
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert "endpoints" in response.json()

def test_user_workflow():
    """Test complete user workflow: create, authenticate, access protected"""
    # Create user
    user_data = {
        "username": "testuser",
        "email": "test@example.com", 
        "password": "testpassword"
    }
    create_res = requests.post(f"{BASE_URL}/users/", json=user_data)
    assert create_res.status_code == 200
    
    # Get auth token
    auth_res = requests.post(
        f"{BASE_URL}/token",
        data={"username": "testuser", "password": "testpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert auth_res.status_code == 200
    token = auth_res.json().get("access_token")
    assert token is not None
    
    # Access protected endpoint
    users_res = requests.get(
        f"{BASE_URL}/users/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert users_res.status_code == 200
    assert isinstance(users_res.json(), list)

def teardown_module():
    """Clean up test data"""
    requests.delete(f"{BASE_URL}/users/testuser")