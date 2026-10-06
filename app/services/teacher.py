from app.domain.teacher.model import Teacher
from app.domain.teacher.schema import TeacherCreate, TeacherUpdate
from app.repositories.teacher import ITeacherRepository, teacher_repo
from app.repositories.user import user_repo
from abc import ABC, abstractmethod
from typing import Optional, List
from app.core.exceptions import NotFound, Conflict

class ITeacherService(ABC):
    @abstractmethod
    def list_teacher(self,q: Optional[str] = None) -> List[Teacher]:
        pass

    @abstractmethod
    def get_teacher(self, q: Optional[str] = None) -> List[Teacher]:
        pass

class TeacherService(ITeacherService):

    def __init__(self, repository: ITeacherRepository = teacher_repo):
        self._teacher_repo = repository

    def list_teacher(self, q: Optional[str] = None) -> List[Teacher]:
        return self._teacher_repo.search(q) if q else self._teacher_repo.list_all()

    def get_teacher(self, teacher_id: int) -> Teacher:
        teacher = self._teacher_repo.get(teacher_id)

        if not teacher:
            raise NotFound("Teacher")

        return teacher

    def create_teacher(self, data:TeacherCreate) -> Teacher:
        if self._teacher_repo.find_by_email(data.email):
            raise Conflict("Email already registered!")

        if self._teacher_repo.find_by_phone(data.phone):
            raise Conflict("This phone number already registered!")
        self._validate_user_assignment(data.user_id)
        teacher = Teacher(id=self._teacher_repo.next_id(), **data.model_dump())
        return self._teacher_repo.add(teacher)

    def update_teacher(self, teacher_id: int, data: TeacherUpdate) -> Teacher:
        teacher = self._teacher_repo.get(teacher_id)

        if not teacher:
            raise NotFound("Teachers")

        update_teacher = data.model_dump(exclude_unset=True)
        if "user_id" in update_teacher:
            self._validate_user_assignment(update_teacher["user_id"], teacher_id)
        if "email" in update_teacher:
            existing = self._teacher_repo.find_by_email(update_teacher["email"])
            if existing and existing.id != teacher_id:
                raise Conflict("Email already registered!")

        if "phone" in update_teacher:
            existing_phone = self._teacher_repo.find_by_phone(update_teacher["phone"])
            if existing_phone and existing_phone.id != teacher_id:
                raise Conflict("Phone already registered!")

        for field, value in update_teacher.items():
            setattr(teacher, field, value)

        return self._teacher_repo.update(teacher_id, teacher)

    def _validate_user_assignment(self, user_id: int | None, teacher_id: int | None = None) -> None:
        if user_id is None:
            return
        if user_repo.get(user_id) is None:
            raise NotFound("User")
        if any(
            teacher.user_id == user_id and teacher.id != teacher_id
            for teacher in self._teacher_repo.list_all()
        ):
            raise Conflict("This user account is already assigned to another teacher")

    def delete_teacher(self, teacher_id:int)->Teacher:
        teacher = self._teacher_repo.get(teacher_id)

        if not teacher:
            raise NotFound("Teacher")
        self._teacher_repo.delete(teacher_id)

teacher_service: TeacherService = TeacherService()

def get_teacher_service() -> TeacherService:
    return teacher_service

def list_teacher(q: Optional[str] = None) ->List[Teacher]:
    return teacher_service.list_teacher(q)

def get_teacher(teacher_id: int) -> Teacher:
    return teacher_service.get_teacher(teacher_id)

def create_teacher(data: TeacherCreate) -> Teacher:
    return teacher_service.create_teacher(data)

def update_teacher(teacher_id: int, data: TeacherUpdate) -> Teacher:
    return teacher_service.update_teacher(teacher_id, data)

def delete_teacher(teacher_id: int) -> None:
    return teacher_service.delete_teacher(teacher_id)
