from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class SignUpRequest(BaseModel):
    name: str
    surname: str
    username: str
    password: str
    email: str
