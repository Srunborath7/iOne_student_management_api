from app.domain.attendance.model import Attendance
from app.repositories.base import InMemoryRepository


class AttendanceRepository(InMemoryRepository[Attendance]):
    def next_id(self) -> int:
        return max(self._items, default=0) + 1


attendance_repo = AttendanceRepository()
