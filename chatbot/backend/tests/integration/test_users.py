@pytest.mark.asyncio
async def test_get_users(client, auth_headers):
    response = await client.get("/users/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json()["users"], list)

@pytest.mark.asyncio
async def test_create_user(client, admin_headers):
    test_user = {
        "username": "newtestuser",
        "email": "new@example.com",
        "password": "securepassword123"
    }
    response = await client.post("/users/", json=test_user, headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["message"] == "User created"

@pytest.mark.asyncio
async def test_get_specific_user(client, auth_headers):
    response = await client.get("/users/1", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

@pytest.mark.asyncio
async def test_update_user(client, auth_headers):
