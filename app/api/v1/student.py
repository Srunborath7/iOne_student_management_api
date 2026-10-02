from fastapi import APIRouter
from app.domain.student.schema import StudentOut,StudentCreate, StudentUpdate
from app.services import student as service

router= APIRouter(prefix="/students", tags=["students"])

@router.get("", response_model=list[StudentOut])
def list_students(q: str | None = None):
    return service.list_students(q)

@router.get("/{student_id}", response_model= StudentOut)
def get_student(student_id: int):
    return service.get_student(student_id)

@router.post("",response_model=StudentOut, status_code=201)
def create_student(data: StudentCreate):
    return service.create_student(data)

@router.put("{student_id}", response_model=StudentOut, status_code=200)
def update_student(student_id: int, data: StudentUpdate):
    return service.update_student(student_id, data)

@router.delete("/{student_id}", status_code=200)
def delete_student(student_id: int):
    service.delete_student(student_id)