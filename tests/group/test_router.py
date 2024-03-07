from fastapi import Depends
from sqlalchemy import select
import pytest

from src.database import get_db
from src.models import User


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



@pytest.mark.asyncio
async def test_add_user_to_group(client):
    await client.post("/auth/signup", json={
        "name": "User",
        "surname": "Name",
        "username": "username",
        "email": "email@email.com",
        "password": "password"
    })
    db = Depends(get_db)
    user = await db.execute(select(User).where(User.email == "email@email.com"))
    user_id = user.scalar().id
    response = await client.post("/group/create", json={"name": "one_more"})
    group_id = response.json()["id"]
    response = await client.post(f"/group/{group_id}/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User added to group"
