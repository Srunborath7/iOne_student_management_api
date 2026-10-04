from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=5, max_length=100)


class LoginRequest(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    is_active: bool = True
    role: str = "user"


class LoginResponse(BaseModel):
    message: str = "Login successful"
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserOut


class RegisterResponse(BaseModel):
    message: str = "Registration successful"
    user: UserOut