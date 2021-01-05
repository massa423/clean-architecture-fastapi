from abc import ABCMeta, abstractmethod
from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    parse_obj_as,
)
from typing import Optional

from app.domains.user import User
from app.usecases.users.data import UserOutputData
from app.injector.repository_injector import injector
from app.core.config import settings


class UserUpdateInputData(BaseModel):
    """
    UserUpdateInputData
    """

    name: Optional[str] = Field(
        None,
        min_length=settings.NAME_MIN_LENGTH,
        regex=settings.AVAILABLE_NAME_CHARACTER,
    )
    password: Optional[str] = Field(
        None,
        min_length=settings.PASSWORD_MIN_LENGTH,
        max_length=settings.PASSWORD_MAX_LENGTH,
        regex=settings.AVAILABLE_PASSWORD_CHARACTER,
    )
    email: Optional[EmailStr]


class UserUpdateInteractor(metaclass=ABCMeta):
    """
    UserUpdateInteractor
    """

    @abstractmethod
    def handle(self, id: int, user: UserUpdateInputData) -> Optional[UserOutputData]:
        """
        handle
        """
        pass


class UserUpdateInteractorImpl(UserUpdateInteractor):
    """
    UserUpdateInteractorImpl
    """

    def handle(
        self, id: int, user_input: UserUpdateInputData
    ) -> Optional[UserOutputData]:
        """
        handle
        """

        user = User(
            id=id,
            name=user_input.name,
            password=user_input.password,
            email=user_input.email,
        )

        # Valueが存在する要素のみアップデート対象として抽出する
        data_to_be_updated = user.dict(exclude_none=True)

        # idしかない場合はバリデーションエラー
        if len(data_to_be_updated) == 1:
            raise ValueError(
                f"Specify at least one field to be updated: {', '.join(user_input.dict().keys())}"
            )

        data = injector.user_repository().update_user(data_to_be_updated)

        return parse_obj_as(UserOutputData, data)
