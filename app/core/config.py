from typing import List
from pydantic import BaseSettings, AnyHttpUrl


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

    DATABASE_DIALECT = "postgresql"
    DATABASE_USER = "postgres"
    DATABASE_PASSWORD = "password"
    DATABASE_HOST = "localhost"
    DATABASE_PORT = "15432"
    DATABASE_NAME = "testdb"
    DATABASE_URL = f"{DATABASE_DIALECT}://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"


settings = Settings()
