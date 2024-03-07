import pytest


@pytest.mark.asyncio
async def test_get_users(client):
    await client.post("/auth/signup", json={"name": "John", "surname": "Doe", "username": "johndoe", "password": "password", "email": "hT0Qf@example.com"})
    await client.post("/auth/signup", json={"name": "Jane", "surname": "Doe", "username": "janedoe", "password": "password", "email": "vzRzO@example.com"})
    await client.post("/auth/signup", json={"name": "Robert", "surname": "Doe", "username": "robertdoe", "password": "password", "email": "jJl8j@example.com"})
    
    response = await client.get(
        "/users?page=1&size=2&filter_by_name=john&sort_by=name&order_by=desc"
    )
    assert response.status_code == 200
    


@pytest.mark.asyncio
async def test_update_user(client):
    await client.post("/auth/signup", json={"name": "John", "surname": "Doe", "username": "johndoe", "password": "password", "email": "hT0Qf@example.com"})
    login_response = await client.post(
        "/auth/login", json={"email": "hT0Qf@example.com", "password": "password"}
    )
    print(login_response.json())
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.patch(
        "/user/me", json={"name": "new_name"}, headers=headers
    )
    assert response.status_code == 204
    assert response.json()["name"] == "new_name"

@pytest.mark.asyncio
async def test_delete_user(client):
    login_response = await client.post(
        "/auth/login", json={"email": "jJl8j@example.com", "password": "password"}
    )
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.delete("/user/me", headers=headers)
    assert response.status_code == 200