from datetime import timedelta

from fastapi import Depends, APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from core.schemas import TokenResponse
from fastapi.security import OAuth2PasswordRequestForm
from core.services import AuthService
from core.settings import settings
from core.utils import get_db_session

router = APIRouter(tags=["auth"])


@router.post('/login/', response_model=TokenResponse, status_code=200)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(get_db_session)) -> JSONResponse:
    """
    Эндпойнт для аутентификации пользователя
    """

    auth_service = AuthService(db)
    user = auth_service.authenticate_user(
        form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=settings.access_token_expires_in_minutes)
    access_token = auth_service.create_access_token(
        data={"username": user.email}, expires_delta=access_token_expires
    )

    result = {"access_token": access_token, "token_type": "bearer"}

    return JSONResponse(result)
