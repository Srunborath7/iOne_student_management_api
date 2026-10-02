from app.domain.student.model import Student
from app.repositories.base import InMemoryRepository
from app.data.students_seed import SEED_STUDENTS


class StudentRepository(InMemoryRepository[Student]):

    def __init__(self, seed: list[dict] | None = None):
        super().__init__()

        for row in seed or []:
            student = Student(**row)
            self._items[student.id] = student

    def next_id(self) -> int:
        if not self._items:
            return 1

        return max(self._items.keys()) + 1

    def find_by_email(self, email: str) -> Student | None:
        return next(
            (
                student
                for student in self._items.values()
                if student.email.lower() == email.lower()
            ),
            None
        )

    def search(self, q: str) -> list[Student]:
        q = q.lower()

        return [
            student
            for student in self._items.values()
            if q in student.name.lower()
            or q in student.email.lower()
        ]


student_repo = StudentRepository(seed=SEED_STUDENTS)