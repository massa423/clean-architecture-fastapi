from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.usecases.auth.auth_usecase import Token
from app.core.logger import logger
from app.usecases.auth.auth_usecase import AuthInteractor
from app.depends.usecase_module import auth_interactor_injector

router = APIRouter()


@router.post(
    "/login",
    response_model=Token,
    responses={
        401: {
            "description": "Incorrect username or password",
            "content": {"application/json": {"example": {"detail": "Incorrect username or password"}}},
        },
    },
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_get_interactor: AuthInteractor = Depends(auth_interactor_injector),
) -> Token:
    try:
        token: Token = user_get_interactor.handle(form_data.__dict__)
    except ValueError as e:
        logger.info(e)
        raise HTTPException(status_code=401, detail=str(e), headers={"WWW-Authenticate": "Bearer"})
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return token
