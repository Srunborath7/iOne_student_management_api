from __future__ import annotations
from datetime import date
from typing import Self
from pydantic import BaseModel, ConfigDict, Field, model_validator
from app.domain.enrollment.model import EnrollmentStatus  # adjust to wherever the enum lives


def _check_dates(start: date | None, end: date | None) -> None:
    if start is not None and end is not None and end < start:
        raise ValueError("end_date cannot be before start_date")


class EnrollmentBase(BaseModel):
    student_id: int = Field(gt=0)
    course_id: int = Field(gt=0)
    start_date: date
    end_date: date | None = None
    status: EnrollmentStatus = EnrollmentStatus.PENDING


class EnrollmentCreate(EnrollmentBase):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    @model_validator(mode="after")
    def validate_dates(self) -> Self:
        _check_dates(self.start_date, self.end_date)
        return self


class EnrollmentUpdate(BaseModel):
    """Partial update (PATCH). Only fields that are sent get changed.

    student_id and course_id are intentionally not updatable; to move a
    student to another course, create a new enrollment.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    start_date: date | None = None
    end_date: date | None = None
    status: EnrollmentStatus | None = None

    @model_validator(mode="after")
    def validate_dates(self) -> Self:
        _check_dates(self.start_date, self.end_date)
        return self


class EnrollmentOut(EnrollmentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
