import time

import pytest

@pytest.mark.asyncio
async def test_signup(client):
    response = await client.post(
        "/auth/signup",
        json={
            "name": "John",
            "surname": "Doe",
            "username": "johndoe",
            "password": "password",
            "email": "hT0Qf@example.com",
        },
    )
    assert response.status_code == 201
    assert response.json() == {"detail": "User successfully registered."}


@pytest.mark.asyncio
async def test_signup_wrong_email_format(client):
    response = await client.post(
        "/auth/signup",
        json={
            "name": "John",
            "surname": "Doe",
            "username": "johndoe",
            "password": "password",
            "email": "wrong_email",
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login(client):
    response = await client.post(
        "/auth/login", json={"email": "hT0Qf@example.com", "password": "password"}
    )
    assert response.status_code == 200
    assert response.json()["access_token"] is not None


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    response = await client.post(
        "/auth/login", json={"email": "hT0Qf@example.com", "password": "wrong_password"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate the user."}


@pytest.mark.asyncio
async def test_refresh_token(client):
    login_response = await client.post(
        "/auth/login", json={"email": "hT0Qf@example.com", "password": "password"}
    )
    access_token = login_response.json()["access_token"]
    refresh_token = login_response.json()["refresh_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    time.sleep(1)
    response = await client.post("/auth/refresh_token", headers=headers)
    assert response.status_code == 200
    assert response.json()["access_token"] != access_token
    assert response.json()["refresh_token"] != refresh_token


@pytest.mark.asyncio
async def test_refresh_token_wrong_token(client):
    headers = {"Authorization": f"Bearer wrong_token"}
    response = await client.post("/auth/refresh_token", headers=headers)
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate the user."}

@pytest.mark.asyncio
async def test_reset_password(client, mocker):
    class Mock_RabbitMQ:
        def __init__(self):
            print("Init rabbitMQ")
        async def __aenter__(self):
            print("Connecting")

        async def __aexit__(self, exc_type, exc, tb):
            print("Disconnecting")

        async def publish(self, message: str, routing_key: str):
            print(f"Resetting password for {message}")
    
    def mock_send_email(email):
        print(f"Sending email to {email}")
        
    mocker.patch("src.rabbitmq.RabbitMQ", Mock_RabbitMQ)
    mocker.patch("src.auth.service.send_email", mock_send_email)
        
    login_response = await client.post(
        "/auth/login", json={"email": "hT0Qf@example.com", "password": "password"}
    )
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.post(
        "/auth/reset_password",
        json={
            "email": "hT0Qf@example.com",
            "password": "password",
            "new_password": "new_password",
        },
        headers=headers,
    )
    assert response.status_code == 200



@pytest.mark.asyncio
async def test_reset_password_wrong_password(client):
    login_response = await client.post(
        "/auth/login", json={"email": "hT0Qf@example.com", "password": "new_password"}
    )
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.post(
        "/auth/reset_password",
        json={
            "email": "hT0Qf@example.com",
            "password": "wrong_password",
            "new_password": "new_password",
        },
        headers=headers,
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate the user."}
