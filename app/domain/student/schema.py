from pydantic import BaseModel, ConfigDict, EmailStr, Field

class StudentCreate(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    age: int = Field(ge=15, le= 100)
    phone: str = Field(max_length=11)
    major: str | None = None

class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    email: str | None = None
    phone: str | None = Field(default=None, max_length=11)
    age: int | None = Field(default=None, ge=15, le=100)
    major: str | None = None

class StudentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    age: int
    phone: str
    major: str | None = None