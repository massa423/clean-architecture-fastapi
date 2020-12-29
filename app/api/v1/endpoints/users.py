from fastapi import APIRouter, status, Path
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from app.usecases.users.user_get_usercase import UserOutputData
from app.core.usecase_injector import injector

router = APIRouter()


@router.get("/")
def read_users() -> UserOutputData:
    """
    read_users
    """
    content = injector.user_get_interactor().handle()

    if not content:
        raise HTTPException(status_code=404, detail="users not found")

    return content


@router.get("/{user_id}", response_model=UserOutputData)
def read_user(
    user_id: int = Path(..., title="The ID of the user.", ge=1)
) -> UserOutputData:
    """
    read_user
    """
    content = injector.user_get_interactor().handle(user_id)

    if not content:
        raise HTTPException(status_code=404, detail="user not found")

    return content


@router.post("/{user_name}", status_code=status.HTTP_201_CREATED)
def create_user(user_name: str) -> JSONResponse:
    """
    create_user
    """

    pass


@router.put("/{user_id}")
def update_user() -> None:
    """
    update_user
    """
    pass


@router.delete("/{user_id}")
def delete_user() -> None:
    """
    delete_user
    """
    pass
