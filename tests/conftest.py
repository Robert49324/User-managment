import asyncio
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from async_asgi_testclient import TestClient

from repositories.AWSClient import S3Client
from repositories.RabbitClient import RabbitMQ
from repositories.RedisClient import RedisClient
from src.main import app

# app.dependency_overrides[RabbitMQ] = lambda: AsyncMock()
app.dependency_overrides[S3Client] = lambda: AsyncMock()
app.dependency_overrides[RedisClient] = lambda: AsyncMock()


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[TestClient, None]:
    host, port = "127.0.0.1", "8000"
    scope = {"client": (host, port)}

    async with TestClient(app, scope=scope) as client:
        yield client
