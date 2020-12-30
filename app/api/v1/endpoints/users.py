from fastapi import APIRouter, status, Path
from fastapi.exceptions import HTTPException
from typing import List

from app.usecases.users.user_get_usercase import UserOutputData
from app.usecases.users.user_create_usecase import UserInputData
from app.core.usecase_injector import injector
from app.exceptions.exception import DuplicateError, NoContentError

router = APIRouter()


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
    except NoContentError:
        raise HTTPException(status_code=404, detail="Users not found")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return content


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
def read_user(id: int = Path(..., title="The ID of the user.", ge=1)) -> UserOutputData:
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
def create_user(user: UserInputData) -> UserOutputData:
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


@router.put("/{id}")
def update_user() -> UserOutputData:
    """
    update_user
    """
    pass


@router.delete("/{id}")
def delete_user() -> UserOutputData:
    """
    delete_user
    """
    pass
