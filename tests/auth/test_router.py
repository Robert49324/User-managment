
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


# @pytest.mark.asyncio
# async def test_reset_password(client, mocker):
#     login_response = await client.post(
#         "/auth/login", json={"email": "hT0Qf@example.com", "password": "password"}
#     )
#     access_token = login_response.json()["access_token"]
#     headers = {"Authorization": f"Bearer {access_token}"}
#     response = await client.post(
#         "/auth/reset_password",
#         json={
#             "email": "hT0Qf@example.com",
#             "password": "password",
#             "new_password": "new_password",
#         },
#         headers=headers,
#     )
#     assert response.status_code == 200

@pytest.mark.asyncio
async def test_reset_password(client, mocker):
    mock_rabbitmq_enter = mocker.patch("repositories.RabbitClient.RabbitMQ.__aenter__", return_value=mocker.AsyncMock())
    mock_rabbitmq_exit = mocker.patch("repositories.RabbitClient.RabbitMQ.__aexit__", return_value=None)
    mock_rabbitmq_publish = mocker.patch("repositories.RabbitClient.RabbitMQ.publish", return_value=None)

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

    mock_rabbitmq_enter.assert_called()
    mock_rabbitmq_publish.assert_called()
    
@pytest.mark.asyncio
async def test_reset_password(client, mocker):
    # Mock the dependencies
    mock_user_repository = mocker.MagicMock()
    mock_redis = mocker.MagicMock()

    # Mock RabbitMQ
    mock_rabbitmq = mocker.MagicMock()
    mock_rabbitmq_instance = mocker.AsyncMock()
    mock_rabbitmq_instance.publish = mocker.AsyncMock()
    mock_rabbitmq.__aenter__ = mocker.AsyncMock(return_value=mock_rabbitmq_instance)
    mock_rabbitmq.__aexit__ = mocker.AsyncMock()

    # Patch the AuthService dependencies
    mocker.patch("your_module.UserRepository", return_value=mock_user_repository)
    mocker.patch("your_module.RedisClient", return_value=mock_redis)
    mocker.patch("your_module.RabbitMQ", return_value=mock_rabbitmq)
    login_response = await client.post(
        "/auth/login", json={"email": "hT0Qf@example.com", "password": "password"}
    )
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    # Make the request to reset the password
    response = await client.post(
        "/auth/reset_password",
        json={
            "email": "example@example.com",
            "password": "current_password",
            "new_password": "new_password",
        },
        headers=headers,
    )

    # Assert that the RabbitMQ methods were called as expected
    mock_rabbitmq.assert_called_once()
    mock_rabbitmq_instance.publish.assert_called_once()

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
