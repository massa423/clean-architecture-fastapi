from abc import ABCMeta, abstractmethod
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

from app.domains.user import User
from app.core.repository_injector import injector


class UserInputData(BaseModel):
    """
    UserInputData
    """

    name: str
    password: str = Field(..., min_length=6, max_length=30)
    email: EmailStr


class UserOutputData(BaseModel):
    """
    UserOutputData
    """

    id: int
    name: str
    password: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime


class UserCreateInteractor(metaclass=ABCMeta):
    """
    UserCreateInteractor
    """

    @abstractmethod
    def handle(self, user: UserInputData) -> Optional[UserOutputData]:
        """
        handle
        """
        pass


class UserCreateInteractorImpl(UserCreateInteractor):
    """
    UserCreateInteractorImpl
    """

    def handle(self, user_input: UserInputData) -> Optional[UserOutputData]:
        """
        handle
        """
        user = User(
            name=user_input.name,
            password=user_input.password,
            email=user_input.email,
        )

        data = injector.user_repository().create_user(
            user.name, user.password, user.email
        )

        response = UserOutputData(
            id=data["id"],
            name=data["name"],
            email=data["email"],
            password=data["password"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )

        return response
