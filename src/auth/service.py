import datetime
from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException
from jose import JWTError, jwt

from auth.config import settings
from database import postgres, redis_
from models import User

from .dependencies import bcrypt_context, oauth2_bearer


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.now() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.now() + timedelta(days=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


def generate_tokens(user):
    access_token = create_access_token(
        {"id": str(user.id), "email": user.email, "role": str(user.role)}
    )
    refresh_token = create_refresh_token({"id": str(user.id)})
    return access_token, refresh_token


def handle_login(user):
    if not user:
        raise HTTPException(status_code=401, detail="Could not validate user.")
    access_token, refresh_token = generate_tokens(user)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        id: str = payload.get("id")
        if id is None:
            raise HTTPException(status_code=401, detail="Could not validate the user.")
        user = postgres.read_by_id(id)

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate the user.")


def authenticate_user(email: str, password: str):
    user = postgres.read(email)
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user


def is_blocked(token: str):
    if redis_.read(token):
        return True
    return False


async def authorize(token: str = Depends(oauth2_bearer)):
    return {token}
