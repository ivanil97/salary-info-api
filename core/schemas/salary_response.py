from pydantic import BaseModel

from datetime import datetime


class SalaryResponse(BaseModel):
    """
    Pydantic-модель, описывающая ответ на запрос о ставке з/п
    """

    id: int
    amount: int
    created_at: datetime
    updated_at: datetime
    promotion_date: datetime
    user_id: int


class SalaryResponseForUser(BaseModel):
    """
    Pydantic-модель, описывающая ответ на запрос о ставке з/п по запросу пользователя
    """

    id: int
    amount: int
    promotion_date: datetime
    user_id: int
