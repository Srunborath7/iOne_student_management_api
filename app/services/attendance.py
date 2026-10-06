from app.core.exceptions import Conflict, NotFound
from app.domain.attendance.model import Attendance
from app.domain.attendance.schema import AttendanceCreate, AttendanceUpdate
from app.repositories.attendance import attendance_repo
from app.repositories.course import course_repo
from app.repositories.student import student_repo


class AttendanceService:
    def __init__(self, repository=attendance_repo):
        self._repo = repository

    def list(self):
        return self._repo.list_all()

    def get(self, attendance_id: int) -> Attendance:
        attendance = self._repo.get(attendance_id)
        if attendance is None:
            raise NotFound("Attendance record")
        return attendance

    def create(self, data: AttendanceCreate) -> Attendance:
        if student_repo.get(data.student_id) is None:
            raise NotFound("Student")
        if course_repo.get(data.course_id) is None:
            raise NotFound("Course")
        if any(
            row.student_id == data.student_id and row.course_id == data.course_id and row.date == data.date
            for row in self.list()
        ):
            raise Conflict("Attendance already exists for this student, course, and date")
        return self._repo.add(Attendance(id=self._repo.next_id(), **data.model_dump()))

    def update(self, attendance_id: int, data: AttendanceUpdate) -> Attendance:
        attendance = self.get(attendance_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(attendance, field, value)
        return self._repo.update(attendance_id, attendance)

    def delete(self, attendance_id: int) -> None:
        self.get(attendance_id)
        self._repo.delete(attendance_id)


attendance_service = AttendanceService()


def get_attendance_service() -> AttendanceService:
    return attendance_service
