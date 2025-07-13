import pytest
from fastapi import status

INCORRECT_USER_DATA = {
    "first_name": "Vasya",
    "last_name": "Sidorov",
    "password": "12345678",
}


@pytest.mark.asyncio
async def test_register_user_with_correct_data(client, login_as_admin, employee_user):
    """Тест для проверки создания нового сотрудника с корректными данными"""

    # Логинимся как админ
    token = login_as_admin

    # Регистрируем нового сотрудника
    response = client.post(
        "/register/",
        json=employee_user,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {'message': 'Новый сотрудник создан', 'user_id': response.json()['user_id']}

    # Пытаемся зарегистрировать его еще раз
    response = client.post(
        "/register/",
        json=employee_user,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_register_user_with_incorrect_data(client, login_as_admin):
    """Тест для проверки создания нового сотрудника с некорректными данными"""

    # Логинимся как админ
    token = login_as_admin

    # Регистрируем нового сотрудника
    response = client.post(
        "/register/",
        json=INCORRECT_USER_DATA,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422
