from fastapi import APIRouter

from app.api.v1 import student
from app.api.v1 import auth

api_router = APIRouter()
api_router.include_router(student.router)
api_router.include_router(auth.router)