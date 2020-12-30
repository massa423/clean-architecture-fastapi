from abc import ABCMeta, abstractmethod
from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    SecretStr,
    parse_obj_as,
)
from datetime import datetime
from typing import Optional
from app.domains.user import User
from app.core.repository_injector import injector
from app.core.config import settings


class UserInputData(BaseModel):
    """
    UserInputData
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


class UserUpdateInteractor(metaclass=ABCMeta):
    """
    UserUpdateInteractor
    """

    @abstractmethod
    def handle(self, id: int, user: UserInputData) -> Optional[UserOutputData]:
        """
        handle
        """
        pass


class UserUpdateInteractorImpl(UserUpdateInteractor):
    """
    UserUpdateInteractorImpl
    """

    def handle(self, id: int, user_input: UserInputData) -> Optional[UserOutputData]:
        """
        handle
        """
        print(user_input)
        user = User(
            id=id,
            name=user_input.name,
            password=user_input.password,
            email=user_input.email,
        )

        user_dict = user.dict()
        data_to_be_updated = {}

        # Valueが存在する要素のみアップデート対象として抽出する
        for k, v in user_dict.items():
            if v:
                data_to_be_updated[k] = v

        # idしかない場合はバリデーションエラー
        if len(data_to_be_updated) == 1:
            raise ValueError(f"need at least one field to be updated: {user_input}")

        data = injector.user_repository().update_user(data_to_be_updated)

        response = parse_obj_as(UserOutputData, data)

        return response
