import sys
from auth.config import settings

sys.path.append("..")

import datetime
from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException
from jose import JWTError, jwt


from database import redis
from models import User

from .dependencies import bcrypt_context, oauth2_bearer


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.now() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.datetime.now() + timedelta(days=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)], db):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        id: str = payload.get("id")
        if id is None:
            raise HTTPException(status_code=401, detail="Could not validate the user.")
        user = db.query(User).filter_by(id=id).first()

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate the user.")


def authenticate_user(email: str, password: str, db):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user


def is_blocked(token: str):
    if redis.exists(token):
        return True
    return False


async def authorize(token: str = Depends(oauth2_bearer)):
    return {token}
