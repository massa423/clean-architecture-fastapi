from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class User(BaseModel):
    """
    User
    """

    id: Optional[int]
    name: Optional[str] = Field(None, min_length=1)
    password: Optional[str] = Field(
        None,
        min_length=1,
    )
    email: Optional[EmailStr]
