import pytest
from fastapi.testclient import TestClient

from core.main import app


@pytest.fixture
def client():
    """
    Фикстура для создания HTTP-клиента
    """
    client = TestClient(app)

    return client
