from typing import Annotated

from fastapi import APIRouter, Depends

from configs.dependencies import authorize, get_current_user
from models.UserModel import User
from schemas.AuthSchemas import (LoginRequest, ResetPasswordRequest,
                                 SignUpRequest, Token)
from services.AuthService import AuthService

auth = APIRouter(prefix="/auth", tags=["Auth module"])


@auth.post("/signup", status_code=201)
async def signup(user: SignUpRequest, authService: AuthService = Depends()):
    print(user.model_dump())
    return await authService.signup(user)


@auth.post("/login")
async def login(form_data: LoginRequest, authService: AuthService = Depends()):
    print(form_data.model_dump())
    return await authService.login(form_data)


@auth.post("/refresh_token")
async def refresh_token(token: Token, authService: AuthService = Depends()):
    return await authService.refresh_token(token.token)


@auth.post("/reset_password", status_code=200)
async def reset_password(
    request: ResetPasswordRequest,
    token: str = Depends(authorize),
    authService: AuthService = Depends(),
):
    return await authService.reset_password(request, token)
