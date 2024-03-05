import asyncio
import os
import sys
from typing import AsyncGenerator, Generator
from unittest.mock import MagicMock

import pytest
import pytest_asyncio
from amqp_mock import create_amqp_mock
from async_asgi_testclient import TestClient

from src.config import TestSettings, get_settings
from src.main import app


def get_settings_override():
    return TestSettings()


# class RabbitMqMock:
#     def __init__(self):
#         pass

#     async def __aenter__(self):
#         pass

#     async def __aexit__(self, exc_type, exc, tb):
#         pass

#     async def publish(self, message: str, routing_key: str):
#         pass


# def get_rabbitmq_override():
#     return RabbitMqMock()


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[TestClient, None]:
    host, port = "127.0.0.1", "8000"
    scope = {"client": (host, port)}
    app.dependency_overrides[get_settings] = get_settings_override
    # app.dependency_overrides[get_rabbitmq] = get_rabbitmq_override
    async with TestClient(app, scope=scope) as client:
        yield client
