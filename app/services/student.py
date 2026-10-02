from app.domain.student.model import Student
from app.domain.student.schema import StudentCreate, StudentUpdate
from app.repositories.student import student_repo
from app.core.exceptions import NotFound, Conflict

def list_students(q: str | None = None) -> Student:
    return student_repo.search(q) if q else student_repo.list_all()

def get_student(student_id: int) -> Student:
    student = student_repo.get(student_id)
    if not student:
        raise NotFound("Student")
    return student

def create_student(data: StudentCreate) -> Student:
    if student_repo.find_by_email(data.email):
        raise Conflict("Email already registered")
    student = Student(id=student_repo.next_id(),**data.model_dump())
    return student_repo.add(student)

def update_student(student_id: int, data: StudentUpdate) -> Student:
    student = student_repo.get(student_id)

    if not student:
        raise NotFound("Student")
    update_data = data.model_dump(exclude_unset=True)

    if "email" in update_data:
        existing = student_repo.find_by_email(update_data["email"])

        if existing and existing.id != student_id:
            raise Conflict("Email already registered")

    for field, value in update_data.items():
        setattr(student, field, value)

    return student_repo.update(student_id, student)

def delete_student(student_id: int) -> None:
    student = student_repo.get(student_id)

    if not student:
        raise NotFound("Student")

    student_repo.delete(student_id)