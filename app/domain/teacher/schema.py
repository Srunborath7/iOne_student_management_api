from pydantic import BaseModel, ConfigDict, Field, EmailStr

class TeacherCreate(BaseModel):
    name: str = Field(min_length=2)
    gender: str = Field(max_length=8)
    phone: str = Field(max_length=11)
    age: int = Field(ge=16, le=100)
    email: EmailStr
    address: str | None = None
    note: str | None = None
    user_id: int | None = Field(default=None, gt=0)

class TeacherUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2)
    gender: str | None = Field(default=None, max_length=8)
    phone: str | None = Field(default=None, max_length=11)
    age: int | None = Field(default=None, ge=16, le=100)
    email: EmailStr | None = None
    address: str | None = None
    note: str | None = None
    user_id: int | None = Field(default=None, gt=0)

class TeacherOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int 
    name: str 
    gender: str 
    phone: str
    age: int 
    email: EmailStr
    address: str | None = None
    note: str | None = None
    user_id: int | None = None
