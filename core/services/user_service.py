from typing import List

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from core.models import User
from core.utils import get_password_hash


class UserService:
    """
    Класс для работы с таблицей User в базе данных
    """

    def __init__(self, db):
        self.db = db
        self.approved_roles = ['admin', 'employee']

    def create_user(self, new_user_data: dict) -> User:
        """
        Функция для создания сотрудника в базе данных
        """

        if new_user_data.get('role') not in self.approved_roles:
            raise HTTPException(
                status_code=400,
                detail=f'Пользователь должен иметь одну из ролей: {", ".join(self.approved_roles)}'
            )

        new_user = User(
            first_name=new_user_data.get('first_name'),
            last_name=new_user_data.get('last_name'),
            role=new_user_data.get('role'),
            email=new_user_data.get('email'),
            hashed_password=get_password_hash(new_user_data.get('password'))
        )

        try:
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)

        except IntegrityError:
            raise HTTPException(
                status_code=400,
                detail="Сотрудник с данным email уже зарегистрирован")

        return new_user

    def get_all_users(self) -> List[User]:
        """
        Функция, возвращающая список всех сотрудников
        """

        all_users = self.db.execute(select(User)).scalars().all()

        if all_users:
            return all_users
        else:
            raise HTTPException(status_code=404, detail="Сотрудники не найдены")

    def get_user_by_id(self, user_id: int) -> User:
        """
        Функция, возвращающая информацию о сотруднике по заданному ID
        """

        statement = select(User).where(User.id == user_id)
        user = self.db.execute(statement).scalars().first()

        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="Сотрудник не найден")

    def get_user_by_email(self, user_email: str) -> User:
        """
        Функция, возвращающая информацию о сотруднике по заданному email.
        """

        statement = select(User).where(User.email == user_email)
        user = self.db.execute(statement).scalars().first()

        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="Сотрудник c таким email не найден")
