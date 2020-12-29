from app.interfaces.gateways.user_repository import UserRepository, UserRepositoryImpl


class RepositoryInjector:
    """
    RepositoryInjector
    """

    def user_repository(self) -> UserRepository:
        """
        user_repository
        """
        return UserRepositoryImpl()


injector = RepositoryInjector()
