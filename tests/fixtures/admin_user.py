import pytest

from core.settings import settings


@pytest.fixture
def admin_user():
    admin_user = {
        "email": settings.admin_email,
        "password": settings.admin_password
    }

    return admin_user
