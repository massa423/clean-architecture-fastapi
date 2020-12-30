from app.usecases.users.user_get_usercase import (
    UserGetInteractor,
    UserGetInteractorImpl,
)
from app.usecases.users.user_create_usecase import (
    UserCreateInteractor,
    UserCreateInteractorImpl,
)
from app.usecases.users.user_delete_usecase import (
    UserDeleteInteractor,
    UserDeleteInteractorImpl,
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

    def user_delete_interactor(self) -> UserDeleteInteractor:
        """
        user_delete_interactor
        """
        return UserDeleteInteractorImpl()


injector = UserCaseInjector()
