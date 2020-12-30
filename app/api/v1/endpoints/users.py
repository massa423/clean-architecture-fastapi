from fastapi import APIRouter, status, Path
from fastapi.exceptions import HTTPException
from pydantic import ValidationError
from typing import List

from app.usecases.users.user_get_usercase import UserOutputData as UserGetOutputData
from app.usecases.users.user_create_usecase import (
    UserInputData as UserCreateInputputData,
    UserOutputData as UserCreateOutputData,
)
from app.usecases.users.user_delete_usecase import (
    UserOutputData as UserDeleteOutputData,
)
from app.usecases.users.user_update_usecase import (
    UserInputData as UserUpdateInputData,
    UserOutputData as UserUpdateOutputData,
)
from app.core.usecase_injector import injector
from app.core.config import settings
from app.exceptions.exception import DuplicateError, NoContentError

router = APIRouter()


@router.get(
    "/",
    response_model=List[UserGetOutputData],
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
def read_users() -> UserGetOutputData:
    """
    read_users
    """
    try:
        content = injector.user_get_interactor().handle()
    except NoContentError:
        raise HTTPException(status_code=404, detail="Users not found")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return content


@router.get(
    "/{id}",
    response_model=UserGetOutputData,
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
) -> UserGetOutputData:
    """
    read_user
    """
    try:
        content = injector.user_get_interactor().handle(id)
    except NoContentError:
        raise HTTPException(status_code=404, detail=f"User not found: id={id}")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return content


@router.post(
    "/{name}",
    response_model=UserCreateOutputData,
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
def create_user(user: UserCreateInputputData) -> UserCreateOutputData:
    """
    create_user
    """

    try:
        content = injector.user_create_interactor().handle(user)
    except DuplicateError:
        raise HTTPException(
            status_code=409, detail=f"User or email is already exists: {user}"
        )
    except NoContentError:
        raise HTTPException(
            status_code=204,
            detail=f"User({user}) is created, but data fetch is failed.",
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Create user is failed.")

    return content


@router.put(
    "/{id}",
    response_model=UserUpdateOutputData,
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
    user: UserUpdateInputData,
    id: int = Path(..., title="The ID of the user.", ge=settings.ID_MIN),
) -> UserUpdateOutputData:
    """
    update_user
    """
    try:
        content = injector.user_update_interactor().handle(id, user)
    except DuplicateError:
        raise HTTPException(
            status_code=409, detail=f"User or email is already exists: {user}"
        )
    except NoContentError:
        raise HTTPException(
            status_code=204,
            detail=f"User({user}) is created, but data fetch is failed.",
        )
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Update user is failed.")

    return content


@router.delete(
    "/{id}",
    response_model=UserDeleteOutputData,
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
) -> UserDeleteOutputData:
    """
    delete_user
    """
    try:
        content = injector.user_delete_interactor().handle(id)
    except NoContentError:
        raise HTTPException(status_code=404, detail=f"User not found: id={id}")
    except Exception:
        raise HTTPException(status_code=500, detail="Delete user is failed.")

    return content
