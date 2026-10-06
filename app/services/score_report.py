from app.core.exceptions import Conflict, NotFound
from app.domain.score_report.model import ScoreReport
from app.domain.score_report.schema import ScoreReportCreate, ScoreReportUpdate
from app.repositories.course import course_repo
from app.repositories.score_report import score_report_repo
from app.repositories.student import student_repo


class ScoreReportService:
    def __init__(self, repository=score_report_repo):
        self._repo = repository

    def list(self):
        return self._repo.list_all()

    def get(self, report_id: int) -> ScoreReport:
        report = self._repo.get(report_id)
        if report is None:
            raise NotFound("Score report")
        return report

    def create(self, data: ScoreReportCreate) -> ScoreReport:
        if student_repo.get(data.student_id) is None:
            raise NotFound("Student")
        if course_repo.get(data.course_id) is None:
            raise NotFound("Course")
        if any(r.student_id == data.student_id and r.course_id == data.course_id for r in self.list()):
            raise Conflict("A score report already exists for this student and course")
        return self._repo.add(ScoreReport(id=self._repo.next_id(), **data.model_dump()))

    def update(self, report_id: int, data: ScoreReportUpdate) -> ScoreReport:
        report = self.get(report_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(report, field, value)
        return self._repo.update(report_id, report)

    def delete(self, report_id: int) -> None:
        self.get(report_id)
        self._repo.delete(report_id)


score_report_service = ScoreReportService()


def get_score_report_service() -> ScoreReportService:
    return score_report_service
