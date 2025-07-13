import pytest
from core.database import Base, testing_engine


@pytest.fixture(scope="function", autouse=True)
def testing_db():
    """Фикстура для создания и удаления таблиц в тестовой базе данных для тестов"""

    Base.metadata.create_all(bind=testing_engine)
    yield
    Base.metadata.drop_all(bind=testing_engine)
