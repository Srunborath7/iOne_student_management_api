from dataclasses import dataclass
from datetime import date


@dataclass
class Attendance:
    id: int
    student_id: int
    course_id: int
    date: date
    status: str
    note: str | None = None
