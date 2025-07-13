import pytest


@pytest.fixture
def employee_user():
    employee_user = {
        "first_name": "Ivan",
        "last_name": "Petrov",
        "email": "ivan_petrov@example.com",
        "password": "12345678",
        "role": "employee"
    }

    return employee_user
