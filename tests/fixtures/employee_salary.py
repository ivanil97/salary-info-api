import pytest


@pytest.fixture
def employee_salary():
    employee_salary = {
        "amount": 30000,
        "created_at": "2025-12-31",
        "updated_at": "2025-12-31",
        "promotion_date": "2026-12-31",
        "user_id": 1
    }

    return employee_salary
