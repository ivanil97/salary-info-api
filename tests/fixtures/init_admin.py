import pytest
from core.scripts.init_admin_user import init_admin_user


@pytest.fixture(scope="function", autouse=True)
def create_admin(testing_db):
    """Фикстура для создания администратора перед всеми тестами"""

    init_admin_user()
