from injector import Injector

from app.depends.repository_module import RepositoryModule
from app.usecases.users.user_get_usercase import UserGetInteractor, UserGetInteractorImpl
from app.usecases.users.user_create_usecase import UserCreateInteractor, UserCreateInteractorImpl
from app.usecases.users.user_update_usecase import UserUpdateInteractor, UserUpdateInteractorImpl
from app.usecases.users.user_delete_usecase import UserDeleteInteractor, UserDeleteInteractorImpl
from app.usecases.auth.auth_usecase import AuthInteractor, AuthInteractorImpl


def user_get_interactor_injector() -> UserGetInteractor:
    injector = Injector([RepositoryModule])
    return injector.get(UserGetInteractorImpl)


def user_create_interactor_injector() -> UserCreateInteractor:
    injector = Injector([RepositoryModule])
    return injector.get(UserCreateInteractorImpl)


def user_update_interactor_injector() -> UserUpdateInteractor:
    injector = Injector([RepositoryModule])
    return injector.get(UserUpdateInteractorImpl)


def user_delete_interactor_injector() -> UserDeleteInteractor:
    injector = Injector([RepositoryModule])
    return injector.get(UserDeleteInteractorImpl)


def auth_interactor_injector() -> AuthInteractor:
    injector = Injector([RepositoryModule])
    return injector.get(AuthInteractorImpl)
