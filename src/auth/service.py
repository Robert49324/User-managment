import datetime
from datetime import timedelta
from typing import Annotated

from aio_pika import Message, connect
from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from database import get_db, postgres, redis_
from models import User
from rabbitmq import get_rabbitmq

from .dependencies import bcrypt_context, oauth2_scheme


async def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.now() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


async def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.now() + timedelta(days=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


async def generate_tokens(user: User):
    access_token = await create_access_token(
        {"id": str(user.id), "email": user.email, "role": str(user.role)}
    )
    refresh_token = await create_refresh_token({"id": str(user.id)})
    return access_token, refresh_token


async def handle_login(user: User):
    if not user:
        raise HTTPException(status_code=401, detail="Could not validate user.")
    access_token, refresh_token = await generate_tokens(user)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    token: str = Depends(oauth2_scheme),
):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        id: str = payload.get("id")
        if id is None:
            raise HTTPException(status_code=401, detail="Could not validate the user.")
        user = await postgres.read_by_id(id, db)
        if user is None:
            raise HTTPException(status_code=401, detail="Could not validate the user.")
        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate the user.")


async def authenticate_user(email: str, password: str, db: AsyncSession):
    user: User = await postgres.read(email, db)
    if user is None:
        raise HTTPException(status_code=401, detail="Could not validate the user.")
    if not bcrypt_context.verify(password, user.password):
        raise HTTPException(status_code=401, detail="Could not validate the user.")
    return user


async def verify_password(user: User, password: str):
    if not bcrypt_context.verify(password, user.password):
        raise HTTPException(status_code=401, detail="Could not validate the user.")
    return True


async def is_blocked(token: str = Depends(oauth2_scheme)):
    if await redis_.read(token):
        return True
    return False


async def block_token(token: str = Depends(oauth2_scheme)):
    await redis_.create(token, "blocked")


def authorize(token: str = Depends(oauth2_scheme)):
    print(token)
    return token


async def send_email(email: str, rabbit = Depends(get_rabbitmq)):
    async with rabbit:
        await rabbit.publish(email, "change_email")
