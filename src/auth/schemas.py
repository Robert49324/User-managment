from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class SignUpRequest(BaseModel):
    name: str
    surname: str
    password: str
    phone_number: str
    email: str
