from abc import abstractmethod
from typing import List, Optional
from app.domain.student.model import Student
from app.repositories.base import InMemoryRepository, IRepository
from app.data.students_seed import SEED_STUDENTS


class IStudentRepository(IRepository[Student]):
    """
    Interface for student persistence operations (OOP - Interface Segregation).
    """

    @abstractmethod
    def next_id(self) -> int:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[Student]:
        pass

    @abstractmethod
    def search(self, q: str) -> List[Student]:
        pass


class StudentRepository(InMemoryRepository[Student], IStudentRepository):
    """
    In-memory student repository implementing IStudentRepository.
    """

    def __init__(self, seed: Optional[List[dict]] = None):
        super().__init__()

        for row in seed or []:
            student = Student(**row)
            self._items[student.id] = student

    def next_id(self) -> int:
        if not self._items:
            return 1
        return max(self._items.keys()) + 1

    def find_by_email(self, email: str) -> Optional[Student]:
        clean_email = email.strip().lower()
        return next(
            (
                student
                for student in self._items.values()
                if student.email.lower() == clean_email
            ),
            None,
        )

    def search(self, q: str) -> List[Student]:
        clean_q = q.strip().lower()
        return [
            student
            for student in self._items.values()
            if clean_q in student.name.lower() or clean_q in student.email.lower()
        ]


# Default student repository singleton
student_repo: IStudentRepository = StudentRepository(seed=SEED_STUDENTS)