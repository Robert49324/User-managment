import asyncio
import os
import sys
from typing import AsyncGenerator, Generator
from unittest.mock import MagicMock

import pytest
import pytest_asyncio
from async_asgi_testclient import TestClient

from src.config import TestSettings
from src.main import app
from amqp_mock import create_amqp_mock

def get_settings_override():
    return TestSettings()

@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def mock_amqp():
    async with create_amqp_mock() as mock:
        yield mock

@pytest_asyncio.fixture
async def client() -> AsyncGenerator[TestClient, None]:
    host, port = "127.0.0.1", "8000"
    scope = {"client": (host, port)}
    async with TestClient(app, scope=scope) as client:
        yield client
