from typing import Annotated

from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from database import postgres

from .dependencies import bcrypt_context, oauth2_bearer


async def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)], db: AsyncSession
):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        id: str = payload.get("id")
        if id is None:
            raise HTTPException(status_code=401, detail="Could not validate the user.")
        user = await postgres.read_by_id(id, db)

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate the user.")


async def get_id(token: Annotated[str, Depends(oauth2_bearer)], db: AsyncSession):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        id: str = payload.get("id")
        if id is None:
            raise HTTPException(status_code=401, detail="Could not validate the user.")
        return id
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate the user.")


async def authorize(token: str = Depends(oauth2_bearer)):
    return token
