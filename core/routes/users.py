from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from core.models import User
from core.schemas import UserCreateRequest, UserResponse
from core.services import UserService, AuthService
from core.utils import get_db_session

router = APIRouter(tags=["users"])


@router.post('/register/', status_code=201)
async def register_user(new_user_data: UserCreateRequest,
                        db: Session = Depends(get_db_session),
                        current_user: User = Depends(AuthService.get_current_user)) -> JSONResponse:
    """
    Эндпоинт для создания нового сотрудника
    """

    if current_user.role != 'admin':
        raise HTTPException(
            status_code=401,
            detail="У вас нет прав для совершения этого действия")

    user_service = UserService(db)
    new_user = user_service.create_user(new_user_data.model_dump())

    return JSONResponse({'message': 'Новый сотрудник создан', 'user_id': new_user.id}, status_code=201)


@router.get("/users/", response_model=List[UserResponse], status_code=200)
async def get_users(db: Session = Depends(get_db_session),
                    current_user: User = Depends(AuthService.get_current_user)):
    """
    Эндпоинт для получения списка сотрудников
    """

    if current_user.role != 'admin':
        raise HTTPException(
            status_code=401,
            detail="У вас нет прав для совершения этого действия")

    user_service = UserService(db)
    users = user_service.get_all_users()

    return users


@router.get("/users/{user_id}/", response_model=UserResponse, status_code=200)
async def get_user_by_id(user_id: int,
                         db: Session = Depends(get_db_session),
                         current_user: User = Depends(AuthService.get_current_user)):
    """
    Эндпоинт для получения сотрудника по ID
    """

    if current_user.role != 'admin':
        raise HTTPException(
            status_code=401,
            detail="У вас нет прав для совершения этого действия")

    user_service = UserService(db)
    users = user_service.get_user_by_id(user_id)

    return users
