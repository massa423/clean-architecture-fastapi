from abc import ABCMeta, abstractmethod
from pydantic import parse_obj_as
from typing import Optional

from app.domains.user import User
from app.usecases.users.data import UserOutputData
from app.injector.repository_injector import injector


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

        return parse_obj_as(UserOutputData, data)
