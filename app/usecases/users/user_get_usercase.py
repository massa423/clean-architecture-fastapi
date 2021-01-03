from abc import ABCMeta, abstractmethod
from typing import Union, List, Optional
from pydantic import parse_obj_as

from app.domains.user import User
from app.usecases.users.data import UserOutputData
from app.core.repository_injector import injector


class UserGetInteractor(metaclass=ABCMeta):
    """
    UserGetUsecase
    """

    @abstractmethod
    def handle(self, id: int) -> Optional[Union[UserOutputData, List[UserOutputData]]]:
        """
        handle
        """
        pass


class UserGetInteractorImpl(UserGetInteractor):
    """
    UserGetInteractorImpl
    """

    def handle(
        self, id: int = 0
    ) -> Optional[Union[UserOutputData, List[UserOutputData]]]:
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
        data = injector.user_repository().find_users()

        response = []

        for d in data:
            response.append(parse_obj_as(UserOutputData, d))

        return response

    def __find_user_by_id(self, id: int) -> Optional[UserOutputData]:
        """
        __find_user_by_id
        """

        user = User(id=id)
        data = injector.user_repository().find_user_by_id(user.id)

        return parse_obj_as(UserOutputData, data)
