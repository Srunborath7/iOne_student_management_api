from abc import abstractmethod
from typing import List, Optional

from app.data.enrollment_seed import SEED_ENROLLMENT
from app.domain.enrollment.model import Enrollment
from app.repositories.base import InMemoryRepository, IRepository


class IEnrollmentRepository(IRepository[Enrollment]):
    @abstractmethod
    def next_id(self) -> int:
        pass

    @abstractmethod
    def find_by_student_id(self, student_id: int) -> List[Enrollment]:
        pass

    @abstractmethod
    def find_by_course_id(self, course_id: int) -> List[Enrollment]:
        pass

    @abstractmethod
    def search(self, q: str) -> List[Enrollment]:
        pass


class EnrollmentRepository(InMemoryRepository[Enrollment], IEnrollmentRepository):
    def __init__(self, seed: Optional[List[dict]] = None):
        super().__init__()
        for row in seed or []:
            enrollment = Enrollment(**row)
            self._items[enrollment.id] = enrollment

    def next_id(self) -> int:
        return max(self._items, default=0) + 1

    def find_by_student_id(self, student_id: int) -> List[Enrollment]:
        return [item for item in self._items.values() if item.student_id == student_id]

    def find_by_course_id(self, course_id: int) -> List[Enrollment]:
        return [item for item in self._items.values() if item.course_id == course_id]

    def search(self, q: str) -> List[Enrollment]:
        query = q.strip().lower()
        if not query:
            return self.list_all()
        return [
            item
            for item in self._items.values()
            if query in item.status.value
            or query in str(item.student_id)
            or query in str(item.course_id)
        ]


enrollment_repo: IEnrollmentRepository = EnrollmentRepository(seed=SEED_ENROLLMENT)
