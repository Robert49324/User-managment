from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: str
    password: str


class SignUpRequest(BaseModel):
    name: str
    surname: str
    username: str
    password: str
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    password: str
    new_password: str
