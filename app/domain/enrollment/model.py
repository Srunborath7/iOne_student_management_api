from __future__ import annotations

import enum
from dataclasses import dataclass
from datetime import date


class EnrollmentStatus(str, enum.Enum):  # use enum.StrEnum on Python 3.11+
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    DROPPED = "dropped"


@dataclass
class Enrollment:
    id: int
    student_id: int
    course_id: int
    start_date: date
    end_date: date | None = None
    status: EnrollmentStatus = EnrollmentStatus.PENDING

    def __post_init__(self) -> None:
        if self.end_date is not None and self.end_date < self.start_date:
            raise ValueError("end_date cannot be before start_date")
