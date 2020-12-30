from app.usecases.users.user_get_usercase import (
    UserGetInteractor,
    UserGetInteractorImpl,
)
from app.usecases.users.user_create_usecase import (
    UserCreateInteractor,
    UserCreateInteractorImpl,
)


class UserCaseInjector:
    """
    UserCaseInjector
    """

    def user_get_interactor(self) -> UserGetInteractor:
        """
        user_get_interactor
        """
        return UserGetInteractorImpl()

    def user_create_interactor(self) -> UserCreateInteractor:
        """
        user_create_interactor
        """
        return UserCreateInteractorImpl()


injector = UserCaseInjector()
