from abc import ABCMeta, abstractmethod
from pydantic import BaseModel, Field, EmailStr, SecretStr, parse_obj_as
from datetime import datetime
from typing import Optional

from app.domains.user import User
from app.core.repository_injector import injector
from app.core.config import settings


class UserInputData(BaseModel):
    """
    UserInputData
    """

    name: str = Field(
        None,
        min_length=settings.NAME_MIN_LENGTH,
        regex=settings.AVAILABLE_NAME_CHARACTER,
    )
    password: str = Field(
        ...,
        min_length=settings.PASSWORD_MIN_LENGTH,
        max_length=settings.PASSWORD_MAX_LENGTH,
        regex=settings.AVAILABLE_PASSWORD_CHARACTER,
    )
    email: EmailStr


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

        return parse_obj_as(UserOutputData, data)
