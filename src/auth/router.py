from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from auth.service import (authenticate_user, authorize, block_token,
                          get_current_user, handle_login, is_blocked,
                          send_email, verify_password)
from database import get_db, postgres
from logger import logger
from models import User

from .dependencies import bcrypt_context
from .schemas import LoginRequest, ResetPasswordRequest, SignUpRequest

auth = APIRouter(prefix="/auth", tags=["Auth module"])


@auth.post("/signup", status_code=201)
async def signup(user: SignUpRequest, db: Annotated[AsyncSession, Depends(get_db)]):
    if await postgres.read(user.email, db) is None:
        logger.info(f"User {user.email} has been registrated")
        user = User(
            name=user.name,
            surname=user.surname,
            username=user.username,
            password=bcrypt_context.hash(user.password),
            email=user.email,
        )
        await postgres.create(user, db)
        return {"detail": "User successfully registered."}
    else:
        raise HTTPException(status_code=409, detail="User already exists.")


@auth.post("/login")
async def login(form_data: LoginRequest, db: Annotated[AsyncSession, Depends(get_db)]):
    user = await authenticate_user(form_data.email, form_data.password, db)
    logger.info(f"Logging in {form_data.email}")
    return await handle_login(user)


@auth.post("/refresh_token")
async def refresh_token(
    db: Annotated[AsyncSession, Depends(get_db)],
    refresh_token: str = Depends(authorize),
):
    print(refresh_token)
    if await is_blocked(refresh_token):
        return HTTPException(status_code=403, detail="Token is blocked")
    await block_token(refresh_token)
    print(refresh_token)
    user = await get_current_user(db=db, token=refresh_token)
    logger.info(f"Refreshing token: {refresh_token}")
    return await handle_login(user)


@auth.post("/reset_password", status_code=200)
async def reset_password(
    db: Annotated[AsyncSession, Depends(get_db)],
    request: ResetPasswordRequest,
    user: User = Depends(get_current_user),
):
    if await verify_password(user, request.password):
        await postgres.update(
            {"password": bcrypt_context.hash(request.new_password)}, db, user.id
        )
        await send_email(request.email)
    return {"detail": "Password successfully reset."}
