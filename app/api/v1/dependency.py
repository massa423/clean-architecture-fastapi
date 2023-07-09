from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.exceptions.exception import NoContentError
from app.usecases.users.data import UserOutputData
from app.core.logger import logger
from app.lib.jwt import get_id_from_token
from app.usecases.users.user_get_usercase import UserGetInteractor
from app.depends.usecase_module import user_get_interactor_injector

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/token/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_get_interactor: UserGetInteractor = Depends(user_get_interactor_injector),
) -> UserOutputData:
    """
    get_current_user
    """

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        id = get_id_from_token(token)
    except Exception as e:
        logger.info(f"Could not validate credentials: {e}")
        raise credentials_exception

    try:
        user = user_get_interactor.handle(int(id))
    except NoContentError as e:
        logger.info(f"Could not validate credentials: {e}")
        raise credentials_exception
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return user
