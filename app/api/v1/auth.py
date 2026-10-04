# app/api/v1/auth.py
from fastapi import APIRouter, Depends, status

from app.api.v1.dependencies import get_current_active_user
from app.domain.user.model import User
from app.domain.user.schema import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    UserOut,
)
from app.services.auth import AuthService, get_auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def register(
    data: RegisterRequest,
    service: AuthService = Depends(get_auth_service),
):
    """
    Registers a new user and returns user info.
    """
    user = service.register(data)
    return UserOut.model_validate(user)


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate and receive access token",
)
def login(
    data: LoginRequest,
    service: AuthService = Depends(get_auth_service),
):
    """
    Authenticates username and password and returns a JWT Bearer access token.
    """
    return service.login(data)


@router.get(
    "/me",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    summary="Get current authenticated user profile using token",
)
def get_current_user_profile(
    current_user: User = Depends(get_current_active_user),
):
    """
    Decodes the Bearer token in the Authorization header and returns current user info.
    """
    return UserOut.model_validate(current_user)


@router.get(
    "/{user_id}",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    summary="Get user details by ID",
)
def get_user(
    user_id: int,
    service: AuthService = Depends(get_auth_service),
):
    """
    Look up a user by ID.
    """
    user = service.get_user(user_id)
    return UserOut.model_validate(user)