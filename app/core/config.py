import os

from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings
    """

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = ["http://localhost"]  # type: ignore

    ID_MIN: int = 1

    NAME_MIN_LENGTH: int = 4
    AVAILABLE_NAME_CHARACTER: str = r"^[0-9a-zA-Z_-]+$"

    PASSWORD_MIN_LENGTH: int = 6
    PASSWORD_MAX_LENGTH: int = 30
    AVAILABLE_PASSWORD_CHARACTER: str = "^[a-zA-Z0-9\\|:;\"'<>,.?/`~!@#$%^&*()_+-={}\\[\\]]+$"

    @validator("PASSWORD_MIN_LENGTH")
    @classmethod
    def password_requires_at_least_6_characters(cls, v: int) -> int:
        """
        password_requires_at_least_6_characters
        """
        if v < 6:
            raise ValueError("PASSWORD_MIN_LENGTH must be greater than 6.")
        return v

    # データベース関連設定
    DATABASE_DIALECT: str = os.getenv("DATABASE_DIALECT", "sqlite")
    DATABASE_USER: str = os.getenv("DATABASE_USER", "admin")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "password")
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT: str = os.getenv("DATABASE_PORT", "5432")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "testdb")

    if DATABASE_DIALECT == "sqlite":
        DATABASE_URL: str = "sqlite:///sample_db.sqlite3"
    else:
        DATABASE_URL = (
            f"{DATABASE_DIALECT}://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
        )

    # JWT関連設定
    JWT_SECRET_KEY: str = os.getenv(
        "JWT_SECRET_KEY",
        "abcdefg0123456789",
    )
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 30))


settings = Settings()
