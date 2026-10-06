from abc import abstractmethod
from typing import List, Optional
from app.domain.teacher.model import Teacher
from app.repositories.base import InMemoryRepository, IRepository
from app.data.teacher_seed import SEED_TEACHER

class ITeacherRepository(IRepository[Teacher]):

    @abstractmethod
    def next_id(self) -> int:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[Teacher]:
        pass

    @abstractmethod
    def find_by_phone(self, phone: str) -> Optional[Teacher]:
        pass

    @abstractmethod
    def search(self, q: str) -> List[Teacher]:
        pass

class TeacherRepository(InMemoryRepository[Teacher], IRepository):

    def __init__(self, seed: Optional[List[dict]] = None):
        super().__init__()

        for row in seed or []:
            teacher = Teacher(**row)
            self._items[teacher.id] = teacher

    def next_id(self) -> int:
        if not self._items:
            return 1
        return max(self._items.keys()) + 1

    def find_by_email(self, email: str) -> Optional[Teacher]:
        for teacher in self._items.values():
            if teacher.email.lower() == email.lower():
                return teacher

        return None

    def find_by_phone(self, phone: str) -> Optional[Teacher]:
        for teacher in self._items.values():
            if teacher.phone == phone:
                return teacher

        return None

    def search(self, q: str) -> List[Teacher]:
        q = q.lower().strip()

        return [
            teacher
            for teacher in self._items.values()
            if q in teacher.name.lower()
            or q in teacher.email.lower()
            or q in teacher.phone
        ]

teacher_repo: ITeacherRepository = TeacherRepository(seed=SEED_TEACHER)