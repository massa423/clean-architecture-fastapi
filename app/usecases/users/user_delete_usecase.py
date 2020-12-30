from abc import ABCMeta, abstractmethod
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from app.domains.user import User
from app.core.repository_injector import injector


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


class UserDeleteInteractor(metaclass=ABCMeta):
    """
    UserDeleteInteractor
    """

    @abstractmethod
    def handle(self, id: int) -> Optional[UserOutputData]:
        """
        handle
        """
        pass


class UserDeleteInteractorImpl(UserDeleteInteractor):
    """
    UserDeleteInteractorImpl
    """

    def handle(self, id: int) -> Optional[UserOutputData]:
        """
        handle
        """
        user = User(id=id)

        data = injector.user_repository().delete_user(user.id)

        response = UserOutputData(
            id=data["id"],
            name=data["name"],
            email=data["email"],
            password=data["password"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )

        return response
