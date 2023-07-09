from injector import Module, Binder

from app.interfaces.gateways.user_repository import UserRepository, UserRepositoryImpl


class RepositoryModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interface=UserRepository, to=UserRepositoryImpl)  # type: ignore
