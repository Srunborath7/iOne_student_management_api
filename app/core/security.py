# app/core/security.py
from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
import bcrypt
import jwt

from app.core.config import settings
from app.core.exceptions import Unauthorized


class IPasswordHasher(ABC):
    """
    Abstract Interface for Password Hashing Strategy (OOP - Abstraction).
    """

    @abstractmethod
    def hash(self, password: str) -> str:
        """Hash a plain text password."""
        pass

    @abstractmethod
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain text password against a hash."""
        pass


class BcryptPasswordHasher(IPasswordHasher):
    """
    Concrete implementation of IPasswordHasher using Bcrypt (OOP - Polymorphism & Encapsulation).
    """

    def hash(self, password: str) -> str:
        # Bcrypt maximum length is 72 bytes
        pwd_bytes = password.encode("utf-8")[:72]
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        try:
            pwd_bytes = plain_password.encode("utf-8")[:72]
            hash_bytes = hashed_password.encode("utf-8")
            return bcrypt.checkpw(pwd_bytes, hash_bytes)
        except (ValueError, TypeError):
            return False


class ITokenService(ABC):
    """
    Abstract Interface for Token Operations (OOP - Abstraction).
    """

    @abstractmethod
    def create_access_token(
        self, subject: str | int, claims: Optional[Dict[str, Any]] = None, expires_delta: Optional[timedelta] = None
    ) -> str:
        """Generate a signed access token."""
        pass

    @abstractmethod
    def decode_token(self, token: str) -> Dict[str, Any]:
        """Decode and validate a signed token."""
        pass


class JWTTokenService(ITokenService):
    """
    Concrete implementation of ITokenService using JWT (OOP - Encapsulation).
    """

    def __init__(
        self,
        secret_key: str = settings.JWT_SECRET_KEY,
        algorithm: str = settings.JWT_ALGORITHM,
        default_expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    ):
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._default_expire_minutes = default_expire_minutes

    def create_access_token(
        self, subject: str | int, claims: Optional[Dict[str, Any]] = None, expires_delta: Optional[timedelta] = None
    ) -> str:
        now = datetime.now(timezone.utc)
        if expires_delta:
            expire = now + expires_delta
        else:
            expire = now + timedelta(minutes=self._default_expire_minutes)

        payload: Dict[str, Any] = {
            "sub": str(subject),
            "iat": int(now.timestamp()),
            "exp": int(expire.timestamp()),
        }

        if claims:
            payload.update(claims)

        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def decode_token(self, token: str) -> Dict[str, Any]:
        try:
            return jwt.decode(
                token,
                self._secret_key,
                algorithms=[self._algorithm],
            )
        except jwt.ExpiredSignatureError:
            raise Unauthorized("Token has expired")
        except jwt.InvalidTokenError:
            raise Unauthorized("Invalid authentication token")


# Singleton / Default instances for Dependency Injection
password_hasher: IPasswordHasher = BcryptPasswordHasher()
token_service: ITokenService = JWTTokenService()


# Backward-compatible convenience functions
def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hasher.verify(plain_password, hashed_password)


def create_access_token(
    subject: str | int, claims: Optional[Dict[str, Any]] = None, expires_delta: Optional[timedelta] = None
) -> str:
    return token_service.create_access_token(subject, claims, expires_delta)


def decode_access_token(token: str) -> Dict[str, Any]:
    return token_service.decode_token(token)