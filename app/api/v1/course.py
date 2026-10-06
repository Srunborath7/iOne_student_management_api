from fastapi import APIRouter, Depends, status
from typing import List,Optional
from app.domain.course.schema import CourseOut, CourseGroupOut, CourseCreate, CourseUpdate
from app.services.course import CourseService, get_course_service

router = APIRouter(prefix="/courses", tags=["Course"])

@router.get("", response_model=List[CourseGroupOut])
def list_courses(q: Optional[str] = None,service: CourseService = Depends(get_course_service), ):
    return service.list_course_groups(q)

@router.get("/{course_id}", response_model=CourseGroupOut)
def get_student(course_id: int, service: CourseService = Depends(get_course_service)):
    return service.get_course_group(course_id)

@router.post("", response_model=CourseOut, status_code= status.HTTP_201_CREATED)
def create_course(data: CourseCreate, service: CourseService = Depends(get_course_service)):
    return service.create_course(data)

@router.put("/{course_id}", response_model=CourseOut, status_code=200)
def update_course(course_id: int, data: CourseUpdate, service: CourseService = Depends(get_course_service)):
    return service.update_course(course_id, data)

@router.delete("/{course_id}", status_code=200)
def delete_course(course_id: int,service: CourseService = Depends(get_course_service)):
    service.delete_course(course_id)
    return {"message" : f"Course {course_id} deleted successfull!"}
