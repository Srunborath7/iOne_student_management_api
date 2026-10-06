from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.course.model import Course
from app.repositories.course import ICourseRepository, course_repo
from app.core.exceptions import Conflict, NotFound
from app.domain.course.schema import CourseCreate, CourseUpdate
from app.repositories.enrollment import enrollment_repo
from app.repositories.student import student_repo
from app.repositories.teacher import teacher_repo

class ICourseService(ABC):

    @abstractmethod
    def list_course(self, q: Optional[str] = None) -> list[Course]:
        pass

class CourseService(ICourseService):

    def __init__(self, repository: ICourseRepository = course_repo):
        self._course_repo = repository

    def list_course(self, q: Optional[str] = None) -> List[Course]:
        return self._course_repo.search(q) if q else self._course_repo.list_all()

    def list_course_groups(self, q: Optional[str] = None) -> list[dict]:
        return [self._course_group(course) for course in self.list_course(q)]

    def get_course_group(self, course_id: int) -> dict:
        course = self.get_course(course_id)
        return self._course_group(course)

    @staticmethod
    def _course_group(course: Course) -> dict:
        teacher = teacher_repo.get(course.teacher_id)
        students_by_id = {
            enrollment.student_id: student_repo.get(enrollment.student_id)
            for enrollment in enrollment_repo.find_by_course_id(course.id)
        }
        return {
            "id": course.id,
            "name": course.name,
            "status": course.status,
            "teacher_id": course.teacher_id,
            "teacher_name": teacher.name if teacher else None,
            "start_date": course.start_date,
            "end_date": course.end_date,
            "description": course.description,
            "classroom": course.classroom,
            "students": [
                {"id": student.id, "name": student.name}
                for student in students_by_id.values()
                if student is not None
            ],
        }

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
        return self._course_repo.update(course_id, course)

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
