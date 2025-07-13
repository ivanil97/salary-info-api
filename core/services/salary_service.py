from datetime import datetime, timedelta
from typing import List

from fastapi import HTTPException
from sqlalchemy import select

from core.models import Salary
from core.services import UserService
from core.settings import settings


class SalaryService:
    """
    Класс для работы с таблицей Salary в базе данных
    """

    def __init__(self, db):
        self.db = db
        self.user_service = UserService(db)

    def create_salary(self, new_salary_data: dict,
                      promotion_period=settings.default_promotion_period) -> Salary:
        """
        Функция для создания ставки зарплаты в базе данных
        """

        user_id = new_salary_data.get('user_id')
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Сотрудник не найден")

        promotion_date = new_salary_data.get('promotion_date')
        if promotion_date is None:
            promotion_date = datetime.utcnow() + timedelta(days=promotion_period)

        new_salary = Salary(
            amount=new_salary_data.get('amount'),
            created_at=new_salary_data.get('created_at'),
            updated_at=new_salary_data.get('updated_at'),
            promotion_date=promotion_date,
            user_id=user_id
        )

        self.db.add(new_salary)
        self.db.commit()
        self.db.refresh(new_salary)

        return new_salary

    def get_all_salaries(self) -> List[Salary]:
        """
        Функция, возвращающая список всех ставок зарплаты
        """

        all_salaries = self.db.execute(select(Salary)).scalars().all()

        if all_salaries:
            return all_salaries
        else:
            raise HTTPException(status_code=404, detail="Ставки зарплаты не найдены")

    def get_user_salary(self, user_id) -> List[Salary]:
        """
        Функция, возвращающая список всех ставок зарплаты сотрудника по ID
        """

        statement = select(Salary).where(Salary.user_id == user_id)
        user_salaries = self.db.execute(statement).scalars().all()

        if user_salaries:
            return user_salaries
        else:
            raise HTTPException(status_code=404, detail="Ставки зарплаты не найдены")
