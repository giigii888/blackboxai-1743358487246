import requests
import pytest

BASE_URL = "http://localhost:8000"

def test_root_endpoint():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert "endpoints" in response.json()

def test_user_flow():
    # Test user creation
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }
    create_res = requests.post(f"{BASE_URL}/users/", json=user_data)
    assert create_res.status_code == 201
    
    # Test authentication
    auth_res = requests.post(
        f"{BASE_URL}/token",
        data={"username": "testuser", "password": "testpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert auth_res.status_code == 200
    token = auth_res.json()["access_token"]
    
    # Test protected endpoint
    users_res = requests.get(
        f"{BASE_URL}/users/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert users_res.status_code == 200
    assert isinstance(users_res.json(), list)

if __name__ == "__main__":
    pytest.main(["-v", __file__])