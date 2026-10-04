# app/services/auth.py
from abc import ABC, abstractmethod
from typing import Optional

from app.core.config import settings
from app.core.exceptions import Conflict, NotFound, Unauthorized
from app.core.security import (
    IPasswordHasher,
    ITokenService,
    password_hasher,
    token_service,
)
from app.domain.user.model import User
from app.domain.user.schema import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    UserOut,
)
from app.repositories.user import IUserRepository, user_repo


class IAuthService(ABC):
    """
    Abstract Interface for Authentication Service (OOP - Abstraction).
    """

    @abstractmethod
    def register(self, data: RegisterRequest) -> User:
        """Register a new user."""
        pass

    @abstractmethod
    def login(self, data: LoginRequest) -> LoginResponse:
        """Authenticate user and generate access token."""
        pass

    @abstractmethod
    def get_user(self, user_id: int) -> User:
        """Retrieve user by ID."""
        pass

    @abstractmethod
    def get_current_user(self, token: str) -> User:
        """Verify token and return current authenticated user."""
        pass


class AuthService(IAuthService):
    """
    Authentication Service implementing IAuthService (OOP - Encapsulation & Dependency Injection).
    """

    def __init__(
        self,
        repository: IUserRepository = user_repo,
        token_mgr: ITokenService = token_service,
        hasher: IPasswordHasher = password_hasher,
        expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    ):
        self._user_repo = repository
        self._token_service = token_mgr
        self._hasher = hasher
        self._expire_minutes = expire_minutes

    def register(self, data: RegisterRequest) -> User:
        username = data.username.strip()
        existing_user = self._user_repo.find_by_username(username)
        if existing_user:
            raise Conflict("Username already registered!")

        user = User(
            id=self._user_repo.next_id(),
            username=username,
            password=self._hasher.hash(data.password),
            role="user",
            is_active=True,
        )
        return self._user_repo.add(user)

    def login(self, data: LoginRequest) -> LoginResponse:
        username = data.username.strip()
        user = self._user_repo.find_by_username(username)

        if not user:
            raise Unauthorized("Invalid username or password")

        if not self._hasher.verify(data.password, user.password):
            raise Unauthorized("Invalid username or password")

        if not user.is_active:
            raise Unauthorized("Account is disabled")

        # Generate JWT access token with user details
        access_token = self._token_service.create_access_token(
            subject=str(user.id),
            claims={
                "username": user.username,
                "role": user.role,
            },
        )

        return LoginResponse(
            message="Login successful",
            access_token=access_token,
            token_type="bearer",
            expires_in=self._expire_minutes * 60,
            user=UserOut.model_validate(user),
        )

    def get_user(self, user_id: int) -> User:
        user = self._user_repo.get(user_id)
        if not user:
            raise NotFound("User")
        return user

    def get_current_user(self, token: str) -> User:
        payload = self._token_service.decode_token(token)
        user_id_raw = payload.get("sub")
        if not user_id_raw:
            raise Unauthorized("Invalid authentication token payload")

        try:
            user_id = int(user_id_raw)
        except (ValueError, TypeError):
            raise Unauthorized("Invalid user ID in token")

        user = self._user_repo.get(user_id)
        if not user:
            raise Unauthorized("User not found or deleted")

        if not user.is_active:
            raise Unauthorized("User account is inactive")

        return user


# Singleton instance
auth_service: AuthService = AuthService()


def get_auth_service() -> AuthService:
    """Dependency provider for FastAPI."""
    return auth_service


# Functional delegates for backward compatibility
def register(data: RegisterRequest) -> User:
    return auth_service.register(data)


def login(data: LoginRequest) -> LoginResponse:
    return auth_service.login(data)


def get_user(user_id: int) -> User:
    return auth_service.get_user(user_id)


def get_current_user(token: str) -> User:
    return auth_service.get_current_user(token)