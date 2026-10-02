from fastapi import APIRouter, status

from app.domain.user.schema import (
    RegisterRequest,
    LoginRequest,
    UserOut,
    LoginResponse
)
from app.services import auth as auth_service

router = APIRouter(prefix="/auth",tags=["Auth"])

@router.post("/register",response_model=UserOut,status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest):
    return auth_service.register(data)

@router.post("/login",response_model=LoginResponse,status_code=status.HTTP_200_OK)
def login(data: LoginRequest):
    user = auth_service.login(data)
    return LoginResponse(message="Login successful", user=UserOut.model_validate(user))

@router.get("/{user_id}",response_model=UserOut)
def get_user(user_id: int):
    return auth_service.get_user(user_id)