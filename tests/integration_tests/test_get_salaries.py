import pytest
from fastapi import status

ADDITIONAL_USER_SALARY = {
    "amount": 10000,
    "created_at": "2026-01-01",
    "updated_at": "2026-01-01",
    "promotion_date": "2026-12-31",
    "user_id": 1
}


@pytest.mark.asyncio
async def test_get_salaries(client, login_as_admin, employee_salary):
    """Тест для проверки эндпоинта для получения списка зарплат"""

    # Логинимся как админ
    token = login_as_admin

    # Создаем новые ставки зарплаты
    response = client.post(
        "/salary/",
        json=employee_salary,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == status.HTTP_201_CREATED

    response = client.post(
        "/salary/",
        json=ADDITIONAL_USER_SALARY,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == status.HTTP_201_CREATED

    # Получаем список всех ставок зарплаты
    get_response = client.get(
        "/salary/",
        headers={"Authorization": f"Bearer {token}"}
    )

    data = get_response.json()
    assert get_response.status_code == status.HTTP_200_OK
    assert len(data) == 2
    assert all(salary["amount"] for salary in data)
    assert all(salary["user_id"] == employee_salary["user_id"] for salary in data)
