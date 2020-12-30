from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    """
    User
    """

    id: Optional[int]
    name: Optional[str]
    password: Optional[str]
    email: Optional[EmailStr]
