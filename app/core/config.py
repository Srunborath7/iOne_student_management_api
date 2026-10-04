from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """
    Application Settings utilizing OOP encapsulation and Pydantic validation.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    PROJECT_NAME: str = "iOne Student Management API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # JWT Authentication Configuration
    JWT_SECRET_KEY: str = "ione-super-secret-jwt-key-2026-auth-token-salt"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # CORS configuration for web clients
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "*"
    ]


settings = Settings()
