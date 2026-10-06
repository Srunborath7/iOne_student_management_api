from __future__ import annotations
import enum
from dataclasses import dataclass
from datetime import date


class CourseStatus(str, enum.Enum): 
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    DROPPED = "dropped"

@dataclass
class Course:
    id: int
    name: str
    teacher_id: int
    start_date: date
    description: str | None
    classroom: str
    status: CourseStatus = CourseStatus.PENDING
    end_date: date | None = None

    def __post_init__(self) -> None:
        if self.end_date is not None and self.end_date < self.start_date:
            raise ValueError("end_date cannot be before start_date")
