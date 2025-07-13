from typing import List, Optional
from pydantic import BaseModel
from core.schemas.salary_response import SalaryResponse


class UserResponse(BaseModel):
    """
    Pydantic-модель, описывающая ответ на запрос о сотруднике
    """

    id: int
    first_name: str
    last_name: str
    role: str
    email: str
    salary: Optional[List[SalaryResponse]] = None
