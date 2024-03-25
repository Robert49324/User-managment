import pytest
from fastapi import HTTPException
from jose import ExpiredSignatureError, JWTError
from unittest.mock import MagicMock, AsyncMock

from models.UserModel import User
from services.AuthService import AuthService

@pytest.fixture
def auth_service():
    return AuthService(
        userRepository=AsyncMock(),
        redis=AsyncMock(),
        rabbit=AsyncMock()
    )

@pytest.mark.asyncio
async def test_create_access_token(auth_service):
    data = {"id": "1", "email": "test@example.com", "role": "user"}
    token = await auth_service.create_access_token(data)
    assert isinstance(token, str)

@pytest.mark.asyncio
async def test_create_refresh_token(auth_service):
    data = {"id": "1"}
    token = await auth_service.create_refresh_token(data)
    assert isinstance(token, str)

@pytest.mark.asyncio
async def test_generate_tokens(auth_service):
    user = User(id="1", email="test@example.com", role="user")
    access_token, refresh_token = await auth_service.generate_tokens(user)
    assert isinstance(access_token, str)
    assert isinstance(refresh_token, str)

@pytest.mark.asyncio
async def test_handle_login(auth_service):
    user = User(id="1", email="test@example.com", role="user")
    auth_service.generate_tokens = AsyncMock(return_value=("access_token", "refresh_token"))
    result = await auth_service.handle_login(user)
    assert result == {
        "access_token": "access_token",
        "refresh_token": "refresh_token",
        "token_type": "bearer",
    }

@pytest.mark.asyncio
async def test_authenticate_user(auth_service):
    auth_service.userRepository.read = AsyncMock(return_value=None)
    with pytest.raises(HTTPException):
        await auth_service.authenticate_user("test@example.com", "password")

@pytest.mark.asyncio
async def test_is_blocked(auth_service):
    auth_service.redis.read = AsyncMock(return_value=True)
    assert await auth_service.is_blocked("token")

@pytest.mark.asyncio
async def test_block_token(auth_service):
    await auth_service.block_token("token")
    auth_service.redis.create.assert_called_once_with("token", "blocked")

@pytest.mark.asyncio
async def test_signup(auth_service):
    auth_service.userRepository.read = AsyncMock(return_value=None)
    auth_service.userRepository.create = AsyncMock()
    result = await auth_service.signup(MagicMock())
    assert result == {"detail": "User successfully registered."}

@pytest.mark.asyncio
async def test_login(auth_service):
    auth_service.authenticate_user = AsyncMock(return_value=User())
    auth_service.handle_login = AsyncMock(return_value={"access_token": "token"})
    result = await auth_service.login(MagicMock())
    assert result == {"access_token": "token"}

@pytest.mark.asyncio
async def test_refresh_token(auth_service):
    auth_service.is_blocked = AsyncMock(return_value=False)
    auth_service.block_token = AsyncMock()
    auth_service.handle_login = AsyncMock(return_value={"access_token": "token"})
    result = await auth_service.refresh_token("refresh_token")
    assert result == {"access_token": "token"}

@pytest.mark.asyncio
async def test_reset_password(auth_service):
    auth_service.verify_password = AsyncMock(return_value=True)
    auth_service.userRepository.update = AsyncMock()
    auth_service.send_email = AsyncMock()
    result = await auth_service.reset_password(MagicMock(), "token")
    assert result == {"detail": "Password successfully reset."}
