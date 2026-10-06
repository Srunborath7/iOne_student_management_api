from typing import List, Optional

from fastapi import APIRouter, Depends, status

from app.domain.enrollment.schema import EnrollmentCreate, EnrollmentOut, EnrollmentUpdate
from app.services.enrollment import EnrollmentService, get_enrollment_service

router = APIRouter(prefix="/enrollments", tags=["Enrollment"])


@router.get("", response_model=List[EnrollmentOut])
def list_enrollments(
    q: Optional[str] = None,
    service: EnrollmentService = Depends(get_enrollment_service),
):
    return service.list_enrollments(q)


@router.get("/{enrollment_id}", response_model=EnrollmentOut)
def get_enrollment(
    enrollment_id: int,
    service: EnrollmentService = Depends(get_enrollment_service),
):
    return service.get_enrollment(enrollment_id)


@router.post("", response_model=EnrollmentOut, status_code=status.HTTP_201_CREATED)
def create_enrollment(
    data: EnrollmentCreate,
    service: EnrollmentService = Depends(get_enrollment_service),
):
    return service.create_enrollment(data)


@router.patch("/{enrollment_id}", response_model=EnrollmentOut)
def update_enrollment(
    enrollment_id: int,
    data: EnrollmentUpdate,
    service: EnrollmentService = Depends(get_enrollment_service),
):
    return service.update_enrollment(enrollment_id, data)


@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enrollment(
    enrollment_id: int,
    service: EnrollmentService = Depends(get_enrollment_service),
):
    service.delete_enrollment(enrollment_id)
