from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from core.schemas import SalaryCreateRequest, SalaryResponse, SalaryResponseForUser
from core.models import User
from core.services import SalaryService, AuthService
from core.utils import get_db_session

router = APIRouter(tags=["salary"])


@router.post('/salary/', status_code=201)
async def create_salary(new_salary_data: SalaryCreateRequest,
                        db: Session = Depends(get_db_session),
                        current_user: User = Depends(AuthService.get_current_user)) -> JSONResponse:
    """
    Эндпоинт для создания новой ставки зарплаты
    """

    if current_user.role != 'admin':
        raise HTTPException(
            status_code=401,
            detail="У вас нет прав для совершения этого действия")

    salary_service = SalaryService(db)
    new_salary = salary_service.create_salary(new_salary_data.model_dump())

    return JSONResponse({'message': 'Создана новая ставка заработной платы', 'salary_id': new_salary.id},
                        status_code=201)


@router.get("/salary/", response_model=List[SalaryResponse], status_code=200)
async def get_salaries(db: Session = Depends(get_db_session),
                       current_user: User = Depends(AuthService.get_current_user)):
    """
    Эндпоинт для получения списка ставок зарплаты
    """

    if current_user.role != 'admin':
        raise HTTPException(
            status_code=401,
            detail="У вас нет прав для совершения этого действия")

    salary_service = SalaryService(db)
    salaries = salary_service.get_all_salaries()

    return salaries


@router.get("/my_salary/", response_model=List[SalaryResponseForUser], status_code=200)
async def get_user_salary(db: Session = Depends(get_db_session),
                          current_user: User = Depends(AuthService.get_current_user)):
    """
    Эндпоинт для получения списка ставок зарплаты по ID сотрудника
    """

    salary_service = SalaryService(db)
    user_salaries = salary_service.get_user_salary(current_user.id)

    return user_salaries
