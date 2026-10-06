from pydantic import BaseModel, ConfigDict, Field


class ScoreReportCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    student_id: int = Field(gt=0)
    course_id: int = Field(gt=0)
    assignment_score: float = Field(ge=0)
    midterm_score: float = Field(ge=0)
    final_score: float = Field(ge=0)
    total_score: float = Field(ge=0)
    grade: str = Field(min_length=1)
    remark: str | None = None


class ScoreReportUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    assignment_score: float = Field(default=None, ge=0)
    midterm_score: float = Field(default=None, ge=0)
    final_score: float = Field(default=None, ge=0)
    total_score: float = Field(default=None, ge=0)
    grade: str = Field(default=None, min_length=1)
    remark: str | None = None


class ScoreReportOut(ScoreReportCreate):
    id: int
