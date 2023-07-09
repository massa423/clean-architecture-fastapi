from abc import ABCMeta, abstractmethod
from typing import Union, List, Optional
from pydantic import parse_obj_as
from injector import inject

from app.domains.user import UserBase
from app.usecases.users.data import UserOutputData
from app.interfaces.gateways.user_repository import UserRepository


class UserGetInteractor(metaclass=ABCMeta):
    """
    UserGetUsecase
    """

    @inject
    def __init__(self, repository: UserRepository):
        self.repository = repository

    @abstractmethod
    def handle(self, id: int = 0) -> Optional[Union[UserOutputData, List[UserOutputData]]]:
        """
        handle
        """
        pass


class UserGetInteractorImpl(UserGetInteractor):
    """
    UserGetInteractorImpl
    """

    def handle(self, id: int = 0) -> Optional[Union[UserOutputData, List[UserOutputData]]]:
        """
        handle
        """
        response: Optional[Union[UserOutputData, List[UserOutputData]]]

        if id:
            response = self.__find_user_by_id(id)
        else:
            response = self.__find_users()

        return response

    def __find_users(self) -> Optional[List[UserOutputData]]:
        """
        __find_users
        """
        data = self.repository.find_users()

        response = []

        for d in data:
            response.append(parse_obj_as(UserOutputData, d))

        return response

    def __find_user_by_id(self, id: int) -> Optional[UserOutputData]:
        """
        __find_user_by_id
        """

        user = UserBase(id=id)
        data = self.repository.find_user_by_id(user.id)

        return parse_obj_as(UserOutputData, data)
