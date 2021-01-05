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
from app.usecases.users.user_update_usecase import (
    UserUpdateInteractor,
    UserUpdateInteractorImpl,
)
from app.usecases.auth.auth_usecase import AuthInteractor, AuthInteractorImpl


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

    def user_update_interactor(self) -> UserUpdateInteractor:
        """
        user_update_interactor
        """

        return UserUpdateInteractorImpl()

    def auth_interactor(self) -> AuthInteractor:
        """
        auth_interactor
        """

        return AuthInteractorImpl()


injector = UserCaseInjector()
