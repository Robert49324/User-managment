from typing import Annotated

from fastapi import APIRouter, Depends
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from database import postgres, redis_
from logger import logger
from models import User
from user.service import authorize, get_current_user, get_id

from .db import get_db
from .schemas import UpdateRequest

user = APIRouter(prefix="/user", tags=["User module"])


@user.patch("/me")
async def update(
    db: Annotated[AsyncSession, Depends(get_db)],
    update_request: UpdateRequest,
    token: str = Depends(authorize),
):
    id = await get_id(token, db)
    user : User = await postgres.update(dict(update_request), db, id)
    return user.__dict__


@user.delete("/me")
async def delete_user(
    db: Annotated[AsyncSession, Depends(get_db)], token: str = Depends(authorize)
):
    await postgres.delete(await get_id(token, db), db)


@user.get("/{user_id}")
async def user_info(token: str = Depends(authorize)):
    logger.debug(token)


@user.patch("/{user_id}")
async def update_user(token: str = Depends(authorize)):
    logger.debug(token)
