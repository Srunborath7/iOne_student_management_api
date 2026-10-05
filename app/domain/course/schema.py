from pydantic import BaseModel,Field, ConfigDict

class CourseCreate(BaseModel):
    name: str = Field(min_length=3)
    status: bool = Field(default=True)
    description: str | None = None

class CourseUpdate(BaseModel):
    name: str | None = Field(min_length=3)
    status: bool | None = Field(default=True)
    description: str | None = None

class CourseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : int
    name: str 
    status: bool 
    description: str | None = None