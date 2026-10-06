from datetime import date as Date

from pydantic import BaseModel, ConfigDict, Field


class AttendanceCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    student_id: int = Field(gt=0)
    course_id: int = Field(gt=0)
    date: Date
    status: str = Field(min_length=1)
    note: str | None = None


class AttendanceUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    date: Date = Field(default=None)
    status: str = Field(default=None, min_length=1)
    note: str | None = None


class AttendanceOut(AttendanceCreate):
    id: int
