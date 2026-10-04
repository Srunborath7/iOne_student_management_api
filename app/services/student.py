# app/services/student.py
from abc import ABC, abstractmethod
from typing import List, Optional

from app.core.exceptions import Conflict, NotFound
from app.domain.student.model import Student
from app.domain.student.schema import StudentCreate, StudentUpdate
from app.repositories.student import IStudentRepository, student_repo


class IStudentService(ABC):
    """
    Abstract Interface for Student Service (OOP - Abstraction).
    """

    @abstractmethod
    def list_students(self, q: Optional[str] = None) -> List[Student]:
        pass

    @abstractmethod
    def get_student(self, student_id: int) -> Student:
        pass

    @abstractmethod
    def create_student(self, data: StudentCreate) -> Student:
        pass

    @abstractmethod
    def update_student(self, student_id: int, data: StudentUpdate) -> Student:
        pass

    @abstractmethod
    def delete_student(self, student_id: int) -> None:
        pass


class StudentService(IStudentService):
    """
    Student Service implementing IStudentService (OOP - Encapsulation & Dependency Injection).
    """

    def __init__(self, repository: IStudentRepository = student_repo):
        self._student_repo = repository

    def list_students(self, q: Optional[str] = None) -> List[Student]:
        return self._student_repo.search(q) if q else self._student_repo.list_all()

    def get_student(self, student_id: int) -> Student:
        student = self._student_repo.get(student_id)
        if not student:
            raise NotFound("Student")
        return student

    def create_student(self, data: StudentCreate) -> Student:
        if self._student_repo.find_by_email(data.email):
            raise Conflict("Email already registered")
        student = Student(id=self._student_repo.next_id(), **data.model_dump())
        return self._student_repo.add(student)

    def update_student(self, student_id: int, data: StudentUpdate) -> Student:
        student = self._student_repo.get(student_id)
        if not student:
            raise NotFound("Student")

        update_data = data.model_dump(exclude_unset=True)

        if "email" in update_data:
            existing = self._student_repo.find_by_email(update_data["email"])
            if existing and existing.id != student_id:
                raise Conflict("Email already registered")

        for field, value in update_data.items():
            setattr(student, field, value)

        return self._student_repo.update(student_id, student)

    def delete_student(self, student_id: int) -> None:
        student = self._student_repo.get(student_id)
        if not student:
            raise NotFound("Student")
        self._student_repo.delete(student_id)


# Singleton instance
student_service: StudentService = StudentService()


def get_student_service() -> StudentService:
    """Dependency provider for FastAPI."""
    return student_service


# Functional delegates for backward compatibility
def list_students(q: Optional[str] = None) -> List[Student]:
    return student_service.list_students(q)


def get_student(student_id: int) -> Student:
    return student_service.get_student(student_id)


def create_student(data: StudentCreate) -> Student:
    return student_service.create_student(data)


def update_student(student_id: int, data: StudentUpdate) -> Student:
    return student_service.update_student(student_id, data)


def delete_student(student_id: int) -> None:
    student_service.delete_student(student_id)