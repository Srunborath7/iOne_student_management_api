from pydantic import BaseModel, Field, ConfigDict

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=5)

class LoginRequest(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    role: str

class LoginResponse(BaseModel):
    message: str
    user: UserOut