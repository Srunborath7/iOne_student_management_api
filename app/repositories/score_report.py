from app.domain.score_report.model import ScoreReport
from app.repositories.base import InMemoryRepository


class ScoreReportRepository(InMemoryRepository[ScoreReport]):
    def next_id(self) -> int:
        return max(self._items, default=0) + 1


score_report_repo = ScoreReportRepository()
