from fastapi import APIRouter, Depends, status

from app.domain.attendance.schema import AttendanceCreate, AttendanceOut, AttendanceUpdate
from app.services.attendance import AttendanceService, get_attendance_service


router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.get("", response_model=list[AttendanceOut])
def list_attendance(service: AttendanceService = Depends(get_attendance_service)):
    return service.list()


@router.get("/{attendance_id}", response_model=AttendanceOut)
def get_attendance(attendance_id: int, service: AttendanceService = Depends(get_attendance_service)):
    return service.get(attendance_id)


@router.post("", response_model=AttendanceOut, status_code=status.HTTP_201_CREATED)
def create_attendance(data: AttendanceCreate, service: AttendanceService = Depends(get_attendance_service)):
    return service.create(data)


@router.patch("/{attendance_id}", response_model=AttendanceOut)
def update_attendance(attendance_id: int, data: AttendanceUpdate, service: AttendanceService = Depends(get_attendance_service)):
    return service.update(attendance_id, data)


@router.delete("/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attendance(attendance_id: int, service: AttendanceService = Depends(get_attendance_service)):
    service.delete(attendance_id)
