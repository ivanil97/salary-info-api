from core.models import User
from core.utils import get_password_hash, get_db_session
from core.settings import settings
from sqlalchemy import select


def init_admin_user() -> None:
    """
    Функция для создания администратора при запуске docker-контейнера
    """

    db = next(get_db_session())
    statement = select(User).where(User.email == settings.admin_email)
    if not db.execute(statement).scalars().first():
        admin = User(
            first_name="First",
            last_name="Admin",
            email=settings.admin_email,
            hashed_password=get_password_hash(settings.admin_password),
            role="admin"
        )
        db.add(admin)
        db.commit()


if __name__ == "__main__":
    init_admin_user()
