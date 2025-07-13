from typing import Optional

from pydantic import BaseModel

from datetime import datetime


class SalaryCreateRequest(BaseModel):
    """
    Pydantic-модель, валидирующая запрос на создание нового сотрудника
    """

    amount: int
    promotion_date: Optional[datetime] = None
    user_id: int
