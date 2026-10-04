# app/api/v1/student.py
from typing import List, Optional
from fastapi import APIRouter, Depends, status

from app.domain.student.schema import StudentCreate, StudentOut, StudentUpdate
from app.services.student import StudentService, get_student_service

router = APIRouter(prefix="/students", tags=["students"])


@router.get("", response_model=List[StudentOut])
def list_students(
    q: Optional[str] = None,
    service: StudentService = Depends(get_student_service),
):
    return service.list_students(q)


@router.get("/{student_id}", response_model=StudentOut)
def get_student(
    student_id: int,
    service: StudentService = Depends(get_student_service),
):
    return service.get_student(student_id)


@router.post("", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
def create_student(
    data: StudentCreate,
    service: StudentService = Depends(get_student_service),
):
    return service.create_student(data)


@router.put("/{student_id}", response_model=StudentOut, status_code=status.HTTP_200_OK)
def update_student(
    student_id: int,
    data: StudentUpdate,
    service: StudentService = Depends(get_student_service),
):
    return service.update_student(student_id, data)


@router.delete("/{student_id}", status_code=status.HTTP_200_OK)
def delete_student(
    student_id: int,
    service: StudentService = Depends(get_student_service),
):
    service.delete_student(student_id)
    return {"message": f"Student {student_id} deleted successfully"}