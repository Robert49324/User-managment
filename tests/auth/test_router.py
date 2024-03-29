import time
from unittest.mock import patch, MagicMock, AsyncMock

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
    response = await client.post(
        "/auth/login", json={"email": "hT0Qf@example.com", "password": "password"}
    )
    token = response.json()["access_token"]
    response = await client.post(
        "/auth/refresh_token",
        json={"token": token},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_reset_password(client):
    with patch('repositories.RabbitClient.RabbitMQ') as MockRabbit:
        mock_rabbit_instance = MockRabbit.return_value
        mock_rabbit_instance.__aenter__ = AsyncMock(return_value=mock_rabbit_instance)
        mock_rabbit_instance.__aexit__ = AsyncMock()

        mock_rabbit_instance.publish = MagicMock()
    
        login_response = await client.post(
            "/auth/login", json={"email": "hT0Qf@example.com", "password": "password"}
        )
        print(login_response.json())
        access_token = login_response.json()["access_token"]
        headers = {"Authorization": f"***"}
        response = await client.post(
            "/auth/reset_password",
            json={
                "email": "hT0Qf@example.com",
                "password": "password",
                "new_password": "new_password",
            },
            headers=headers,
        )
        print(response.json())
        assert response.status_code == 200
        mock_rabbit_instance.publish.assert_called_once()


@pytest.mark.asyncio
async def test_reset_password_wrong_password(client):
    login_response = await client.post(
        "/auth/login", json={"email": "hT0Qf@example.com", "password": "new_password"}
    )
    print(login_response.json())
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
    print(response.json())
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate the user."}
