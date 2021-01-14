import os

from typing import List
from pydantic import BaseSettings, AnyHttpUrl, validator


class Settings(BaseSettings):
    """
    Settings
    """

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost"]  # type: ignore

    ID_MIN = 1

    NAME_MIN_LENGTH = 4
    AVAILABLE_NAME_CHARACTER = r"^[0-9a-zA-Z_-]+$"

    PASSWORD_MIN_LENGTH = 6
    PASSWORD_MAX_LENGTH = 30
    AVAILABLE_PASSWORD_CHARACTER = (
        r"^[a-zA-Z0-9\\|:;\"\'<>,.?/`˜!@#$%^&*()_+-=\{\}\[\]]+$"
    )

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
    DATABASE_DIALECT = os.getenv("DATABASE_DIALECT", "sqlite")
    DATABASE_USER = os.getenv("DATABASE_USER", "admin")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "password")
    DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "testdb")

    if DATABASE_DIALECT == "sqlite":
        DATABASE_URL = "sqlite:///sample_db.sqlite3"
    else:
        DATABASE_URL = f"{DATABASE_DIALECT}://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

    # JWT関連設定
    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "abcdefg0123456789",
    )
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 30)
    )


settings = Settings()
