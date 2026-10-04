from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenPayload(BaseModel):
    sub: str
    exp: int
    iat: Optional[int] = None
    username: Optional[str] = None
    role: Optional[str] = None