from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """
    UserBase
    """

    id: int


class User(UserBase):
    """
    User
    """

    id: int | None = None
    name: str = Field(min_length=1)
    password: str = Field(min_length=1)
    email: EmailStr
