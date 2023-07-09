from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBase(BaseModel):
    """
    UserBase
    """

    id: int


class User(UserBase):
    """
    User
    """

    id: Optional[int] = None
    name: str = Field(min_length=1)
    password: str = Field(min_length=1)
    email: EmailStr
