from abc import abstractmethod
from app.repositories.base import InMemoryRepository, IRepository
from typing import Optional, List
from app.domain.enrollment.model import Enrollment
from app.data.enrollment_seed import SEED_ENROLLMENT

class IEnrollmentRepository(IRepository):

    @abstractmethod
    def find_by_course_name(self, name: str) -> Optional[Enrollment]:
        pass

    @abstractmethod
    def find_by_student_name(self, name: str) ->Optional[Enrollment]:
        pass

    @abstractmethod
    def next_id(self) -> int:
        pass

    @abstractmethod
    def search(self, q: str) -> List[Enrollment]:
        pass

class EnrollmentRepository(InMemoryRepository[Enrollment], IRepository):
    def __init__(self, seed):
        super().__init__()

        for row in seed or []:
            enrollment = Enrollment(**row)
            self._items[enrollment.id] = enrollment

    def next_id(self) -> int:
        if not self._items:
            return 1
        return max(self._items.keys()) + 1

enrollment_repo: IEnrollmentRepository = EnrollmentRepository(seed=SEED_ENROLLMENT)