from abc import ABCMeta, abstractmethod
from pydantic import parse_obj_as
from injector import inject

from app.domains.user import UserBase
from app.usecases.users.data import UserOutputData
from app.interfaces.gateways.user_repository import UserRepository


class UserDeleteInteractor(metaclass=ABCMeta):
    """
    UserDeleteInteractor
    """

    @inject
    def __init__(self, repository: UserRepository):
        self.repository = repository

    @abstractmethod
    def handle(self, id: int) -> UserOutputData | None:
        """
        handle
        """
        pass


class UserDeleteInteractorImpl(UserDeleteInteractor):
    """
    UserDeleteInteractorImpl
    """

    def handle(self, id: int) -> UserOutputData | None:
        """
        handle
        """

        user = UserBase(id=id)

        data = self.repository.delete_user(user.id)

        return parse_obj_as(UserOutputData, data)
