from pydantic import BaseModel


class TokenResponse(BaseModel):
    """
    Pydantic-модель, описывающая ответ на запрос о получении токена
    """

    access_token: str
    token_type: str
