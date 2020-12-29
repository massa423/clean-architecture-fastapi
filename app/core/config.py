from typing import List
from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    """
    Settings
    """

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost"]


settings = Settings()
