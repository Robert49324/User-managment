import asyncio
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from async_asgi_testclient import TestClient
from src.aws import get_s3_client

from src.main import app
from src.rabbitmq import get_rabbitmq


def get_rabbitmq_override():
    return AsyncMock()
def get_s3client_override():
    return AsyncMock()


app.dependency_overrides[get_rabbitmq] = get_rabbitmq_override
app.dependency_overrides[get_s3_client] = get_s3client_override

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
