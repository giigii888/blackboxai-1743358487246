import pytest
import requests
from minimal_api_v4 import app

BASE_URL = "http://localhost:8000"

def test_get_users():
    # Get auth token
    auth_res = requests.post(
        f"{BASE_URL}/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    assert auth_res.status_code == 200
    headers = {"Authorization": f"Bearer {auth_res.json()['access_token']}"}
    
    # Test endpoint
    response = requests.get(f"{BASE_URL}/users/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json()["users"], list)

def test_create_user():
    # Get admin token
    admin_res = requests.post(
        f"{BASE_URL}/token",
        data={"username": "admin", "password": "adminpassword"}
    )
    assert admin_res.status_code == 200
    headers = {"Authorization": f"Bearer {admin_res.json()['access_token']}"}
    
    # Test creation
    test_user = {
        "username": "newtestuser",
        "email": "new@example.com",
        "password": "securepassword123"
    }
    response = requests.post(f"{BASE_URL}/users/", json=test_user, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "User created"