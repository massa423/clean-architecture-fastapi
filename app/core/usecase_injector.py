from app.usecases.users.user_get_usercase import (
    UserGetInteractor,
    UserGetInteractorImpl,
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


injector = UserCaseInjector()
