from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import GroupCreate
from src.database import postgres_group, postgres_user, get_db
from src.models import Group
from sqlalchemy import Null


group = APIRouter(prefix="/group", tags=["Group module"])

@group.post("/")
async def create_group(group: GroupCreate, db: AsyncSession = Depends(get_db)):
    if await postgres_group.read(group.name, db):
        raise HTTPException(status_code=400, detail="Group already exists")
    group = Group(**group.dict())
    group = await postgres_group.create(group, db)
    return group


@group.delete("/{group_id}")
async def remove_group(group_id: int, db: AsyncSession = Depends(get_db)):
    if not await postgres_group.read_by_id(group_id, db):
        raise HTTPException(status_code=404, detail="Group not found")
    group = await postgres_group.delete(group_id, db)
    return group


@group.post("/{group_id}/users/{user_id}")
async def add_user_to_group(
    group_id: int, user_id: str, db: AsyncSession = Depends(get_db)
):
    group = await postgres_group.read(group_id, db)
    user = await postgres_user.read_by_id(user_id, db)
    if group and user:
        await postgres_user.update({"group" : group.id},db, user_id)
        return {"message": "User added to group"}

@group.delete("/{group_id}/users/{user_id}")
async def delete_user_from_group(
    group_id: int, user_id: str, db: AsyncSession = Depends(get_db)
):
    group = await postgres_group.read(group_id, db)
    user = await postgres_user.read_by_id(user_id, db)
    if not group and not user:
        raise HTTPException(status_code=404, detail="Group or user not found")
    await postgres_user.update({"group" : Null() }, db, user_id)
