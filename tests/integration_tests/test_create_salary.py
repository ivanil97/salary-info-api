import pytest
from fastapi import status

INCORRECT_SALARY_DATA = {
    "amount": 30000,
    "created_at": "2025-12-31",
}


@pytest.mark.asyncio
async def test_create_salary_with_correct_data(client, login_as_admin, employee_salary):
    """Тест для проверки создания новой ставки зарплаты с корректными данными"""

    # Логинимся как админ
    token = login_as_admin

    # Создаем новую ставку зарплаты
    response = client.post(
        "/salary/",
        json=employee_salary,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {'message': 'Создана новая ставка заработной платы',
                               'salary_id': response.json()['salary_id']}


@pytest.mark.asyncio
async def test_create_salary_with_incorrect_data(client, login_as_admin):
    """Тест для проверки создания нового сотрудника с некорректными данными"""

    # Логинимся как админ
    token = login_as_admin

    # Создаем новую ставку зарплаты
    response = client.post(
        "/salary/",
        json=INCORRECT_SALARY_DATA,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422
