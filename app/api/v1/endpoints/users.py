from fastapi import APIRouter, status, Path, Depends
from fastapi.exceptions import HTTPException
from typing import List

from app.api.v1.dependency import get_current_user
from app.usecases.users.data import UserOutputData
from app.usecases.users.user_create_usecase import UserCreateInputputData
from app.usecases.users.user_update_usecase import UserUpdateInputData
from app.injector.usecase_injector import injector
from app.core.config import settings

from app.core.logger import logger
from app.exceptions.exception import DuplicateError, NoContentError

router = APIRouter()


# [TODO]offsetとlimitの指定
@router.get(
    "/",
    response_model=List[UserOutputData],
    responses={
        404: {
            "description": "Users not found",
            "content": {"application/json": {"example": {"detail": "Users not found"}}},
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {"example": {"detail": "Internal Server Error"}}
            },
        },
    },
)
def read_users() -> UserOutputData:
    """
    read_users
    """

    try:
        content = injector.user_get_interactor().handle()
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
            "content": {
                "application/json": {
                    "example": {"detail": "Incorrect username or password"}
                }
            },
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {"example": {"detail": "Internal Server Error"}}
            },
        },
    },
)
async def read_users_me(
    user: UserOutputData = Depends(get_current_user),
) -> UserOutputData:
    return user


@router.get(
    "/{id}",
    response_model=UserOutputData,
    responses={
        404: {
            "description": "User not found",
            "content": {
                "application/json": {"example": {"detail": "User not found: id=id"}}
            },
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {"example": {"detail": "Internal Server Error"}}
            },
        },
    },
)
def read_user(
    id: int = Path(..., title="The ID of the user.", ge=settings.ID_MIN)
) -> UserOutputData:
    """
    read_user
    """

    try:
        content = injector.user_get_interactor().handle(id)
    except NoContentError as e:
        logger.info(f"NoContentError: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return content


@router.post(
    "/{name}",
    response_model=UserOutputData,
    status_code=status.HTTP_201_CREATED,
    responses={
        204: {
            "description": "User is created, but data fetch is failed.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User(name) is created, but data fetch is failed."
                    }
                }
            },
        },
        409: {
            "description": "User of email is already exists.",
            "content": {
                "application/json": {
                    "example": {"detail": "User or email is already exists: name"}
                }
            },
        },
        500: {
            "description": "Create user is failed",
            "content": {
                "application/json": {"example": {"detail": "Create user is failed."}}
            },
        },
    },
)
def create_user(user: UserCreateInputputData = Depends()) -> UserOutputData:
    """
    create_user
    """

    try:
        content = injector.user_create_interactor().handle(user)
    except DuplicateError as e:
        logger.info(f"DuplicateError: {e}")
        raise HTTPException(
            status_code=409, detail=f"User or email is already exists: {user}"
        )
    except NoContentError:
        logger.warning(
            "NoContentError: User({user}) is created, but data fetch is failed."
        )
        raise HTTPException(
            status_code=204,
            detail=f"User({user}) is created, but data fetch is failed.",
        )
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Create user is failed.")

    return content


@router.put(
    "/{id}",
    response_model=UserOutputData,
    responses={
        204: {
            "description": "User is updated, but data fetch is failed.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User(name) is updated, but data fetch is failed."
                    }
                }
            },
        },
        400: {
            "description": "Bad Request.",
            "content": {
                "application/json": {"example": {"detail": "Invalid request body."}}
            },
        },
        409: {
            "description": "User of email is already exists.",
            "content": {
                "application/json": {
                    "example": {"detail": "User or email is already exists: name"}
                }
            },
        },
        500: {
            "description": "Update user is failed",
            "content": {
                "application/json": {"example": {"detail": "Update user is failed."}}
            },
        },
    },
)
def update_user(
    user: UserUpdateInputData = Depends(),
    id: int = Path(..., title="The ID of the user.", ge=settings.ID_MIN),
) -> UserOutputData:
    """
    update_user
    """

    try:
        content = injector.user_update_interactor().handle(id, user)
    except DuplicateError as e:
        logger.info(f"DuplicateError: {e}")
        raise HTTPException(
            status_code=409, detail=f"User or email is already exists: {user}"
        )
    except NoContentError:
        logger.warning(
            "NoContentError: User({user}) is updated, but data fetch is failed."
        )
        raise HTTPException(
            status_code=204,
            detail=f"User({user}) is updated, but data fetch is failed.",
        )
    except ValueError as e:
        logger.info(f"ValueError: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Update user is failed.")

    return content


@router.delete(
    "/{id}",
    response_model=UserOutputData,
    responses={
        404: {
            "description": "User not found",
            "content": {
                "application/json": {"example": {"detail": "User not found: id=id"}}
            },
        },
        500: {
            "description": "Delete user is failed",
            "content": {
                "application/json": {"example": {"detail": "Delete user is failed."}}
            },
        },
    },
)
def delete_user(
    id: int = Path(..., title="The ID of the user.", ge=settings.ID_MIN)
) -> UserOutputData:
    """
    delete_user
    """

    try:
        content = injector.user_delete_interactor().handle(id)
    except NoContentError:
        logger.info(f"NoContentError: User not found: id={id}")
        raise HTTPException(status_code=404, detail=f"User not found: id={id}")
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Delete user is failed.")

    return content
