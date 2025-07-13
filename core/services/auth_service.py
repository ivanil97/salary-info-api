from datetime import timedelta, datetime
from typing import Union

import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from core.models import User
from core.services import UserService
from core.settings import settings
from core.utils import get_db_session

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"


class AuthService:
    """
    Сервис для аутентификации пользователя
    """

    def __init__(self, db):
        self.user_service = UserService(db)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, received_password: str, hashed_password: str) -> bool:
        """
        Функция для верификации пароля, переданного при аутентификации
        """

        return self.pwd_context.verify(received_password, hashed_password)

    def authenticate_user(self, username: str, password: str) -> Union[bool, User]:
        """
        Функция для аутентификации пользователя
        """

        try:
            user = self.user_service.get_user_by_email(username)
        except HTTPException:
            return False

        if not self.verify_password(password, user.hashed_password):
            return False

        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta) -> str:
        """
        Создает токен для пользователя
        """

        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt

    @staticmethod
    def get_current_user(token: str = Depends(oauth2_schema),
                         db: Session = Depends(get_db_session)) -> User:
        """
        Проверяет, существует ли пользователь, передавший токен, в базе, и возвращает его
        """

        if not token:
            raise HTTPException(
                status_code=401,
                detail="Требуется авторизация",
                headers={"WWW-Authenticate": "Bearer"},
            )

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("username")

            if username is None:
                raise credentials_exception
        except InvalidTokenError:
            raise credentials_exception

        user_service = UserService(db)
        user = user_service.get_user_by_email(username)

        if user is None:
            raise credentials_exception

        return user
