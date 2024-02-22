from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from database import get_db, postgres, redis_
from logger import logger
from models import Group, User
from user.service import authorize, get_current_user, get_id

from .schemas import ReturnUser, UpdateRequest

user = APIRouter(prefix="/user", tags=["User module"])


@user.patch("/me", response_model=ReturnUser)
async def update(
    db: Annotated[AsyncSession, Depends(get_db)],
    update_request: UpdateRequest,
    token: str = Depends(authorize),
):
    id = await get_id(token, db)
    user: User = await postgres.update(dict(update_request), db, id)
    return ReturnUser(
        name=user.name,
        surname=user.surname,
        username=user.username,
        email=user.email,
        phone_number=user.phone_number if user.phone_number else "",
    )


@user.delete("/me")
async def delete_user(
    db: Annotated[AsyncSession, Depends(get_db)], token: str = Depends(authorize)
):
    await postgres.delete(await get_id(token, db), db)


@user.get("/{user_id}", response_model=ReturnUser)
async def user_info(
    user_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    token: str = Depends(authorize),
):
    caller = await get_current_user(token, db)
    if caller.role == "USER":
        raise HTTPException(403, detail="No access")
    user = await postgres.read_by_id(user_id, db)

    if user.group == caller.group:
        return ReturnUser(
            name=user.name,
            surname=user.surname,
            username=user.username,
            email=user.email,
            phone_number=user.phone_number if user.phone_number else "",
        )
    raise HTTPException(403, detail="No access")


@user.patch("/{user_id}", response_model=ReturnUser)
async def update_user(
    update_request: UpdateRequest,
    user_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    token: str = Depends(authorize),
):
    caller = await get_current_user(token, db)
    if caller.role == "USER":
        raise HTTPException(403, detail="No access")
    user = await postgres.read_by_id(user_id, db)

    if user.group == caller.group:
        user: User = await postgres.update(dict(update_request), db, user.id)
        return ReturnUser(
            name=user.name,
            surname=user.surname,
            username=user.username,
            email=user.email,
            phone_number=user.phone_number if user.phone_number else "",
        )
