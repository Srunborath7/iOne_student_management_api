from datetime import date
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.domain.course.model import CourseStatus


def _check_dates(start_date: date, end_date: date | None) -> None:
    if end_date is not None and end_date < start_date:
        raise ValueError("end_date cannot be before start_date")


class CourseCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str = Field(min_length=3)
    status: CourseStatus = CourseStatus.PENDING
    teacher_id: int = Field(gt=0)
    start_date: date
    end_date: date | None = None
    description: str | None = None
    classroom: str = Field(min_length=1, max_length=50)

    @model_validator(mode="after")
    def validate_dates(self) -> Self:
        _check_dates(self.start_date, self.end_date)
        return self


class CourseUpdate(BaseModel):
    """Full replacement schema for PUT; each field must be provided."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str = Field(min_length=3)
    status: CourseStatus
    teacher_id: int = Field(gt=0)
    start_date: date
    end_date: date | None
    description: str | None
    classroom: str = Field(min_length=1, max_length=50)

    @model_validator(mode="after")
    def validate_dates(self) -> Self:
        _check_dates(self.start_date, self.end_date)
        return self


class CourseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    status: CourseStatus
    teacher_id: int
    start_date: date
    end_date: date | None
    description: str | None
    classroom: str


class CourseStudentOut(BaseModel):
    id: int
    name: str


class CourseGroupOut(CourseOut):
    teacher_name: str | None = None
    students: list[CourseStudentOut] = Field(default_factory=list)
