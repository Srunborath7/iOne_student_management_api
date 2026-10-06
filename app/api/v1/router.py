from fastapi import APIRouter

from app.api.v1 import student
from app.api.v1 import auth
from app.api.v1 import course
from app.api.v1 import enrollment
from app.api.v1 import teacher
from app.api.v1 import score_report
from app.api.v1 import attendance

api_router = APIRouter()
api_router.include_router(student.router)
api_router.include_router(auth.router)
api_router.include_router(course.router)
api_router.include_router(enrollment.router)
api_router.include_router(teacher.router)
api_router.include_router(score_report.router)
api_router.include_router(attendance.router)
