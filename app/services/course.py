from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.course.model import Course
from app.repositories.course import ICourseRepository, course_repo
from app.core.exceptions import Conflict, NotFound
from app.domain.course.schema import CourseCreate, CourseUpdate

class ICourseService(ABC):

    @abstractmethod
    def list_course(self, q: Optional[str] = None) -> list[Course]:
        pass

class CourseService(ICourseService):

    def __init__(self, repository: ICourseRepository = course_repo):
        self._course_repo = repository

    def list_course(self, q: Optional[str] = None) -> List[Course]:
        return self._course_repo.search(q) if q else self._course_repo.list_all()

    def get_course(self,student_id: int) -> Course:
        course = self._course_repo.get(student_id)
        if not course:
            raise NotFound("Course")
        return course

    def create_course(self, data: CourseCreate) -> Course:
        if self._course_repo.find_by_name(data.name):
            raise Conflict ("Course this name ready created!")
        course = Course(id=self._course_repo.next_id(), **data.model_dump())
        return self._course_repo.add(course)

    def update_course(self, course_id: int, data: CourseUpdate) -> Course:
        course = self._course_repo.get(course_id)

        if not course:
            raise NotFound("Course")

        update_data = data.model_dump(exclude_unset=True)

        if "name" in update_data:
            existing = self._course_repo.find_by_name(update_data["name"])
            if existing and existing.id != course_id:
                raise Conflict("This Course Name Ready Created!")

        for field, val in update_data.items():
            setattr(course, field, val)

    def delete_course(self, course_id: int) -> None:
        course = self._course_repo.get(course_id)

        if not course:
            raise NotFound("Student")
        self._course_repo.delete(course_id)

course_service: CourseService = CourseService()

def get_course_service() -> CourseService:
    return course_service

def list_course(q: Optional[str] = None) -> List[Course]:
    return course_service.list_course(q)

def get_course(course_id:int) -> Course:
    return course_service.get_course(course_id)

def create_course(data: CourseCreate) -> Course:
    return course_service.create_course(data)

def update_course(course_id: int, data: CourseUpdate) -> Course:
    return course_service.update_course(course_id, data)

def delete_course(course_id: int) -> None:
    course_service.delete_course(course_id)



