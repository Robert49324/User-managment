import pytest
from fastapi import HTTPException
from unittest.mock import AsyncMock, MagicMock
from models.UserModel import User
from schemas.AuthSchemas import LoginRequest, ResetPasswordRequest, SignUpRequest
from services.AuthService import AuthService

@pytest.fixture
def mock_user_repository():
    return AsyncMock()

@pytest.fixture
def mock_redis_client():
    return AsyncMock()

@pytest.fixture
def mock_rabbitmq():
    return AsyncMock()

@pytest.fixture
def auth_service(mock_user_repository, mock_redis_client, mock_rabbitmq):
    return AuthService(
        userRepository=mock_user_repository,
        redis=mock_redis_client,
        rabbit=mock_rabbitmq
    )

@pytest.mark.asyncio
async def test_create_access_token(auth_service):
    user_data = {"id": "1", "email": "test@example.com", "role": "user"}
    token = await auth_service.create_access_token(user_data)
    assert token is not None

@pytest.mark.asyncio
async def test_create_refresh_token(auth_service):
    user_data = {"id": "1"}
    token = await auth_service.create_refresh_token(user_data)
    assert token is not None

@pytest.mark.asyncio
async def test_generate_tokens(auth_service):
    user = User(id="1", email="test@example.com", role="user")
    access_token, refresh_token = await auth_service.generate_tokens(user)
    assert access_token is not None
    assert refresh_token is not None

@pytest.mark.asyncio
async def test_handle_login(auth_service):
    user = User(id="1", email="test@example.com", role="user")
    tokens = await auth_service.handle_login(user)
    assert "access_token" in tokens
    assert "refresh_token" in tokens

@pytest.mark.asyncio
async def test_authenticate_user(auth_service, mock_user_repository):
    mock_user_repository.read.return_value = User(
        id="1", email="test@example.com", role="user"
    )
    user = await auth_service.authenticate_user("test@example.com", "password")
    assert user is not None

@pytest.mark.asyncio
async def test_verify_password(auth_service):
    user = User(id="1", email="test@example.com", role="user", password="$2b$12$2")
    result = await auth_service.verify_password(user, "password")
    assert result

@pytest.mark.asyncio
async def test_is_blocked(auth_service, mock_redis_client):
    mock_redis_client.read.return_value = True
    blocked = await auth_service.is_blocked("token")
    assert blocked

@pytest.mark.asyncio
async def test_block_token(auth_service, mock_redis_client):
    await auth_service.block_token("token")
    mock_redis_client.create.assert_called_once_with("token", "blocked")

@pytest.mark.asyncio
async def test_signup(auth_service, mock_user_repository, mock_rabbitmq):
    request = SignUpRequest(
        name="John",
        surname="Doe",
        username="johndoe",
        email="johndoe@example.com",
        password="password",
    )
    await auth_service.signup(request)
    mock_user_repository.create.assert_called_once()

@pytest.mark.asyncio
async def test_login(auth_service, mock_user_repository):
    request = LoginRequest(email="test@example.com", password="password")
    mock_user_repository.read.return_value = User(
        id="1", email="test@example.com", role="user"
    )
    tokens = await auth_service.login(request)
    assert "access_token" in tokens
    assert "refresh_token" in tokens

@pytest.mark.asyncio
async def test_refresh_token(auth_service, mock_redis_client, mock_user_repository):
    mock_user_repository.read.return_value = User(
        id="1", email="test@example.com", role="user"
    )
    mock_redis_client.read.return_value = False
    tokens = await auth_service.refresh_token("refresh_token")
    assert "access_token" in tokens
    assert "refresh_token" in tokens

@pytest.mark.asyncio
async def test_reset_password(auth_service, mock_user_repository, mock_rabbitmq):
    request = ResetPasswordRequest(
        email="test@example.com", password="password", new_password="new_password"
    )
    user = User(id="1", email="test@example.com", role="user", password="hashed_password")
    mock_user_repository.read.return_value = user
    await auth_service.reset_password(request, "token")
    mock_user_repository.update.assert_called_once()

