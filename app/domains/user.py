from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from app.core.config import settings


class User(BaseModel):
    """
    User
    """

    id: Optional[int]
    name: Optional[str] = Field(None, min_length=4)
    password: Optional[str] = Field(
        None,
        min_length=settings.PASSWORD_MIN_LENGTH,
        regex=settings.AVAILABLE_PASSWORD_CHARACTER,
    )
    email: Optional[EmailStr]
