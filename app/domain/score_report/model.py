from dataclasses import dataclass


@dataclass
class ScoreReport:
    id: int
    student_id: int
    course_id: int
    assignment_score: float
    midterm_score: float
    final_score: float
    total_score: float
    grade: str
    remark: str | None = None
