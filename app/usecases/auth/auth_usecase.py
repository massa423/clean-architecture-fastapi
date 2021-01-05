from abc import ABCMeta, abstractmethod
from typing import Dict
from pydantic import BaseModel
from datetime import timedelta

from app.injector.repository_injector import injector
from app.core.config import settings
from app.lib.security import encrypt_password_to_sha256
from app.lib.jwt import create_access_token
from app.exceptions.exception import NoContentError


class Token(BaseModel):
    """
    Token
    """

    access_token: str
    token_type: str


class AuthInteractor(metaclass=ABCMeta):
    """
    AuthInteractor
    """

    @abstractmethod
    def handle(self, form_data: Dict) -> Token:
        """
        handle
        """
        pass


class AuthInteractorImpl(AuthInteractor):
    """
    AuthInteractorImpl
    """

    def handle(self, form_data: Dict) -> Token:
        """
        handle
        """

        try:
            user = injector.user_repository().find_user_by_name(form_data["username"])
        except NoContentError:
            raise ValueError("Incorrect username or password")

        hashed_password = encrypt_password_to_sha256(form_data["password"])

        if user["password"] != str(hashed_password):
            raise ValueError("Incorrect username or password")

        access_token_expires = timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token = create_access_token(
            data={"sub": str(user["id"])}, expires_delta=access_token_expires
        )

        return Token(access_token=access_token, token_type="bearer")
