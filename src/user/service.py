import io
from typing import Annotated

import aioboto3
from fastapi import Depends, HTTPException, UploadFile
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from database import get_db, postgres_user
from logger import logger

from .dependencies import oauth2_bearer


async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    token: str = Depends(oauth2_bearer),
):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        id: str = payload.get("id")
        print(id)
        if id is None:
            raise HTTPException(status_code=401, detail="Could not validate the user.")
        user = await postgres_user.read_by_id(id, db)
        if user is None:
            raise HTTPException(status_code=401, detail="Could not validate the user.")
        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate the user.")
