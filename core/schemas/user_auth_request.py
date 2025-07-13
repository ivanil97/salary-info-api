from pydantic import BaseModel


class UserAuthRequest(BaseModel):
    """
    Pydantic-модель, валидирующая запрос на авторизацию сотрудника
    """

    email: str
    password: str
