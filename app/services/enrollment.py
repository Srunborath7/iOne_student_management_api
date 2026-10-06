from abc import ABC, abstractmethod
from typing import List, Optional
from fastapi import HTTPException, status

from app.core.exceptions import Conflict, NotFound
from app.domain.enrollment.model import Enrollment
from app.domain.enrollment.schema import EnrollmentCreate, EnrollmentUpdate
from app.repositories.course import ICourseRepository, course_repo
from app.repositories.enrollment import IEnrollmentRepository, enrollment_repo
from app.repositories.student import IStudentRepository, student_repo


class IEnrollmentService(ABC):
    @abstractmethod
    def list_enrollments(self, q: Optional[str] = None) -> List[Enrollment]:
        pass


class EnrollmentService(IEnrollmentService):
    def __init__(
        self,
        repository: IEnrollmentRepository = enrollment_repo,
        students: IStudentRepository = student_repo,
        courses: ICourseRepository = course_repo,
    ):
        self._repo = repository
        self._students = students
        self._courses = courses

    def list_enrollments(self, q: Optional[str] = None) -> List[Enrollment]:
        return self._repo.search(q) if q else self._repo.list_all()

    def get_enrollment(self, enrollment_id: int) -> Enrollment:
        enrollment = self._repo.get(enrollment_id)
        if enrollment is None:
            raise NotFound("Enrollment")
        return enrollment

    def create_enrollment(self, data: EnrollmentCreate) -> Enrollment:
        if self._students.get(data.student_id) is None:
            raise NotFound("Student")
        if self._courses.get(data.course_id) is None:
            raise NotFound("Course")
        if any(
            item.student_id == data.student_id
            and item.course_id == data.course_id
            and item.status.value in ("pending", "active")
            for item in self._repo.list_all()
        ):
            raise Conflict("Student already has a pending or active enrollment in this course")

        enrollment = Enrollment(id=self._repo.next_id(), **data.model_dump())
        return self._repo.add(enrollment)

    def update_enrollment(self, enrollment_id: int, data: EnrollmentUpdate) -> Enrollment:
        enrollment = self.get_enrollment(enrollment_id)
        update_data = data.model_dump(exclude_unset=True)
        start_date = update_data.get("start_date", enrollment.start_date)
        end_date = update_data.get("end_date", enrollment.end_date)
        if end_date is not None and end_date < start_date:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="end_date cannot be before start_date",
            )
        for field, value in update_data.items():
            setattr(enrollment, field, value)
        return self._repo.update(enrollment_id, enrollment)

    def delete_enrollment(self, enrollment_id: int) -> None:
        self.get_enrollment(enrollment_id)
        self._repo.delete(enrollment_id)


enrollment_service = EnrollmentService()


def get_enrollment_service() -> EnrollmentService:
    return enrollment_service
