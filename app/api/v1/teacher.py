from fastapi import APIRouter, Depends, status
from app.domain.teacher.schema import TeacherOut, TeacherUpdate, TeacherCreate
from app.services.teacher import TeacherService, get_teacher_service
from typing import Optional, List

router = APIRouter(prefix="/teachers", tags= ["Teacher"])

@router.get("", response_model= List[TeacherOut])
def list_teacher(q: Optional[str] = None, service: TeacherService = Depends(get_teacher_service)):
    return service.list_teacher(q)

@router.get("/{teacher_id}", response_model=TeacherOut)
def get_teacher(teacher_id: int, service: TeacherService = Depends(get_teacher_service)):
    return service.get_teacher(teacher_id)

@router.post("",response_model=TeacherOut, status_code=status.HTTP_201_CREATED)
def create_teacher(data: TeacherCreate, service: TeacherService = Depends(get_teacher_service)):
    return service.create_teacher(data)

@router.put("/{teacher_id}", response_model=TeacherOut, status_code=status.HTTP_200_OK)
def update_teacher(teacher_id: int, data: TeacherUpdate, service: TeacherService = Depends(get_teacher_service)):
    return service.update_teacher(teacher_id, data)

@router.delete("{teacher_id}", status_code=status.HTTP_200_OK)
def delete_teacher(teacher_id: int, service: TeacherService = Depends(get_teacher_service)):
    service.delete_teacher(teacher_id)
    return {"message" : f"Teacher {teacher_id} deleted successfully!"}