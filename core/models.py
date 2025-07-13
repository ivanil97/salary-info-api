from datetime import datetime
from typing import List, Literal

from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.database import Base


class Salary(Base):
    """
    Модель для хранения данных о ставке зарплаты
    """

    __tablename__ = 'salary'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    promotion_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates='salary')

    def __str__(self):
        return f'Ставка зарплаты {self.id}, сумма: {self.amount} руб., следующее повышение: {self.promotion_date}, сотрудник: {self.user_id}'


class User(Base):
    """
    Модель для хранения данных о сотруднике
    """

    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    role: Mapped[Literal["admin", "employee"]] = mapped_column(String, nullable=False, default='employee')
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(1000))
    salary: Mapped[List["Salary"]] = relationship(back_populates='user')

    def __str__(self):
        return f'Сотрудник {self.id}: {self.first_name} {self.last_name} {self.email}'
