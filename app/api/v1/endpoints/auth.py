from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.usecases.auth.auth_usecase import Token
from app.core.usecase_injector import injector
from app.core.logger import logger

router = APIRouter()


@router.post(
    "/login",
    response_model=Token,
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
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    try:
        token: Token = injector.auth_interactor().handle(form_data.__dict__)
    except ValueError as e:
        logger.info(e)
        raise HTTPException(
            status_code=401, detail=str(e), headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return token
