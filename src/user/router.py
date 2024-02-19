from typing import Annotated

from fastapi import APIRouter, Depends
from jose import JWTError, jwt

from config import settings
from database import postgres, redis_
from logger import logger
from models import User
from user.service import authorize, get_current_user

from .schemas import UpdateRequest

user = APIRouter(prefix="/user", tags=["User module"])


@user.patch("/me")
def update(update_request: UpdateRequest, token: str = Depends(authorize)):
    user = get_current_user(token)
    user = user.__dict__
    for key, value in update_request.model_dump().items():
        if value != None and key in user:
            user[key] = value
    postgres.update(user)


@user.delete("/me")
def delete_user(token: str = Depends(authorize)):
    logger.debug(token)


@user.get("/{user_id}")
def user_info(token: str = Depends(authorize)):
    logger.debug(token)


@user.patch("/{user_id}")
def update_user(token: str = Depends(authorize)):
    logger.debug(token)
