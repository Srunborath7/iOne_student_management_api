# app/api/v1/dependencies.py
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.domain.user.model import User
from app.services.auth import AuthService, get_auth_service

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    service: AuthService = Depends(get_auth_service),
) -> User:
    """
    Extract and validate Bearer token from Authorization header, returning authenticated User.
    """
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return service.get_current_user(credentials.credentials)


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Ensure the authenticated user is active.
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user account",
        )
    return current_user
