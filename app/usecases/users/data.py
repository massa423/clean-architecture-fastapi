from pydantic import BaseModel, SecretStr, EmailStr
from datetime import datetime


class UserOutputData(BaseModel):
    """
    UserOutputData
    """

    id: int
    name: str
    password: SecretStr
    email: EmailStr
    created_at: datetime
    updated_at: datetime
