from typing import Literal
from pydantic import BaseModel


class UserCreateRequest(BaseModel):
    """
    Pydantic-модель, валидирующая запрос на создание нового сотрудника
    """

    first_name: str
    last_name: str
    role: str
    email: str
    password: str
