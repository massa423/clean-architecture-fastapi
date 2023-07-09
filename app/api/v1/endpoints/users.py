from fastapi import APIRouter, status, Path, Depends, Response
from fastapi.exceptions import HTTPException

from app.api.v1.dependency import get_current_user
from app.usecases.users.data import UserOutputData
from app.usecases.users.user_get_usercase import UserGetInteractor
from app.usecases.users.user_create_usecase import UserCreateInputData, UserCreateInteractor
from app.usecases.users.user_update_usecase import UserUpdateInputData, UserUpdateInteractor
from app.usecases.users.user_delete_usecase import UserDeleteInteractor

from app.core.config import settings
from app.core.logger import logger
from app.exceptions.exception import DuplicateError, NoContentError
from app.depends.usecase_module import (
    user_get_interactor_injector,
    user_create_interactor_injector,
    user_update_interactor_injector,
    user_delete_interactor_injector,
)

router = APIRouter()


# TODO: offsetとlimitの指定
@router.get(
    "/",
    response_model=list[UserOutputData],
    responses={
        404: {
            "description": "Users not found",
            "content": {"application/json": {"example": {"detail": "Users not found"}}},
        },
    },
)
def read_users(
    user_get_interactor: UserGetInteractor = Depends(user_get_interactor_injector),
) -> UserOutputData:
    """
    read_users
    """

    try:
        content = user_get_interactor.handle()
    except NoContentError as e:
        logger.info(f"NoContentError: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return content


@router.get(
    "/me",
    response_model=UserOutputData,
    responses={
        401: {
            "description": "Incorrect username or password",
            "content": {"application/json": {"example": {"detail": "Incorrect username or password"}}},
        },
    },
)
def read_users_me(
    user: UserOutputData = Depends(get_current_user),
) -> UserOutputData:
    """
    read_user_me
    """
    return user


@router.get(
    "/{id}",
    response_model=UserOutputData,
    responses={
        404: {
            "description": "User not found",
            "content": {"application/json": {"example": {"detail": "User not found: id=id"}}},
        },
    },
)
def read_user(
    id: int = Path(
        ...,
        title="The ID of the user.",
        ge=settings.ID_MIN,
    ),
    user_get_interactor: UserGetInteractor = Depends(user_get_interactor_injector),
) -> UserOutputData:
    """
    read_user
    """

    try:
        content = user_get_interactor.handle(id)
    except NoContentError as e:
        logger.info(f"NoContentError: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return content


@router.post(
    "/",
    response_model=UserOutputData,
    status_code=status.HTTP_201_CREATED,
    responses={
        204: {
            "description": "User is created, but data fetch is failed.",
        },
        409: {
            "description": "User of email is already exists.",
            "content": {"application/json": {"example": {"detail": "User or email is already exists: name"}}},
        },
    },
)
def create_user(
    user: UserCreateInputData,
    user_create_interactor: UserCreateInteractor = Depends(user_create_interactor_injector),
) -> UserOutputData | Response:
    """
    create_user
    """

    try:
        content = user_create_interactor.handle(user)
    except DuplicateError as e:
        logger.info(f"DuplicateError: {e}")
        raise HTTPException(status_code=409, detail=f"User or email is already exists: {user}")
    except NoContentError:
        logger.warning(f"NoContentError: User({user}) is created, but data fetch is failed.")
        # ステータスコード204はmessage bodyを含めることができない。
        # https://github.com/tiangolo/fastapi/issues/2253
        return Response(status_code=204)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return content


@router.put(
    "/{id}",
    response_model=UserOutputData,
    responses={
        204: {
            "description": "User is updated, but data fetch is failed.",
        },
        400: {
            "description": "Bad Request.",
            "content": {"application/json": {"example": {"detail": "Invalid request body."}}},
        },
        404: {
            "description": "User not found",
            "content": {"application/json": {"example": {"detail": "User not found: id=id"}}},
        },
        409: {
            "description": "User of email is already exists.",
            "content": {"application/json": {"example": {"detail": "User or email is already exists: name"}}},
        },
    },
)
def update_user(
    user: UserUpdateInputData,
    id: int = Path(..., title="The ID of the user.", ge=settings.ID_MIN),
    user_update_interactor: UserUpdateInteractor = Depends(user_update_interactor_injector),
) -> UserOutputData | Response:
    """
    update_user
    """

    try:
        content = user_update_interactor.handle(id, user)
    except DuplicateError as e:
        logger.info(f"DuplicateError: {e}")
        raise HTTPException(status_code=409, detail=f"User or email is already exists: {user}")
    except NoContentError as e:
        if "404" in str(e):
            logger.info(f"NoContentError: User not found: id={id}")
            raise HTTPException(status_code=404, detail=f"User not found: id={id}")
        else:
            logger.warning(f"NoContentError: User({user}) is updated, but data fetch is failed.")
            return Response(status_code=204)
    except ValueError as e:
        logger.info(f"ValueError: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return content


@router.delete(
    "/{id}",
    response_model=UserOutputData,
    responses={
        404: {
            "description": "User not found",
            "content": {"application/json": {"example": {"detail": "User not found: id=id"}}},
        },
    },
)
def delete_user(
    id: int = Path(..., title="The ID of the user.", ge=settings.ID_MIN),
    user_delete_interactor: UserDeleteInteractor = Depends(user_delete_interactor_injector),
) -> UserOutputData:
    """
    delete_user
    """

    try:
        content = user_delete_interactor.handle(id)
    except NoContentError:
        logger.info(f"NoContentError: User not found: id={id}")
        raise HTTPException(status_code=404, detail=f"User not found: id={id}")
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return content
