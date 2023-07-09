from abc import ABCMeta, abstractmethod
from pydantic import BaseModel, Field, EmailStr, parse_obj_as
from typing import Optional

from app.domains.user import User
from app.usecases.users.data import UserOutputData
from app.injector.repository_injector import injector
from app.core.config import settings


class UserCreateInputputData(BaseModel):
    """
    UserCreateInputputData
    """

    name: str = Field(
        ...,
        min_length=settings.NAME_MIN_LENGTH,
        pattern=settings.AVAILABLE_NAME_CHARACTER,
        example="user",
    )
    password: str = Field(
        ...,
        min_length=settings.PASSWORD_MIN_LENGTH,
        max_length=settings.PASSWORD_MAX_LENGTH,
        pattern=settings.AVAILABLE_PASSWORD_CHARACTER,
        example="password",
    )
    email: EmailStr


class UserCreateInteractor(metaclass=ABCMeta):
    """
    UserCreateInteractor
    """

    @abstractmethod
    def handle(self, user: UserCreateInputputData) -> Optional[UserOutputData]:
        """
        handle
        """
        pass


class UserCreateInteractorImpl(UserCreateInteractor):
    """
    UserCreateInteractorImpl
    """

    def handle(self, user_input: UserCreateInputputData) -> Optional[UserOutputData]:
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
