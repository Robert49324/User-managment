import datetime
from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from database import postgres, redis_
from models import User

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
    token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession
):
    try:
        payload: dict = jwt.decode(
            token, settings.secret_key, algorithms=settings.algorithm
        )
        id: str = payload.get("id")
        if id is None:
            raise HTTPException(status_code=401, detail="Could not validate the user.")
        user: User = await postgres.read_by_id(id, db)

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate the user.")


async def authenticate_user(email: str, password: str, db: AsyncSession):
    user: User = await postgres.read(email, db)
    if user is None:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user


async def is_blocked(token: str = Depends(oauth2_scheme)):
    if await redis_.read(token):
        return True
    return False


async def block_token(token: str = Depends(oauth2_scheme)):
    await redis_.create(token, "blocked")


async def authorize(token: str = Depends(oauth2_scheme)):
    return token
