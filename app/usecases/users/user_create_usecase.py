from abc import ABCMeta, abstractmethod
from pydantic import BaseModel, Field, EmailStr, parse_obj_as
from injector import inject

from app.domains.user import User
from app.usecases.users.data import UserOutputData
from app.core.config import settings
from app.interfaces.gateways.user_repository import UserRepository


class UserCreateInputData(BaseModel):
    """
    UserCreateInputData
    """

    name: str = Field(
        ..., min_length=settings.NAME_MIN_LENGTH, pattern=settings.AVAILABLE_NAME_CHARACTER, example="user"
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

    @inject
    def __init__(self, repository: UserRepository):
        self.repository = repository

    @abstractmethod
    def handle(self, user: UserCreateInputData) -> UserOutputData | None:
        """
        handle
        """
        pass


class UserCreateInteractorImpl(UserCreateInteractor):
    """
    UserCreateInteractorImpl
    """

    def handle(self, user_input: UserCreateInputData) -> UserOutputData | None:
        """
        handle
        """

        user = User(
            name=user_input.name,
            password=user_input.password,
            email=user_input.email,
        )

        data = self.repository.create_user(user.name, user.password, user.email)

        return parse_obj_as(UserOutputData, data)
