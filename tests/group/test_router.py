from fastapi import Depends
from sqlalchemy import select
import pytest

@pytest.mark.asyncio
async def test_create_group(client):
    response = await client.post("/group/create", json={"name": "group"})
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Group created"


@pytest.mark.asyncio
async def test_delete_group(client):
    response = await client.post("/group/create", json={"name": "new_group"})
    print(response.json())
    group_id = response.json()["id"]
    response = await client.delete(f"/group/{group_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Group deleted"
