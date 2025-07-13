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
async def test_get_my_salary(client, login_as_admin, employee_user, employee_salary):
    """Тест для проверки эндпоинта для получения списка зарплат"""

    # Логинимся как админ
    token = login_as_admin

    # Создаем нового сотрудника
    user_register_response = client.post(
        "/register/",
        json=employee_user,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert user_register_response.status_code == status.HTTP_201_CREATED

    # Создаем новые ставки зарплаты
    salary_data = employee_salary.copy()
    salary_data['user_id'] = user_register_response.json()['user_id']

    additional_salary_data = ADDITIONAL_USER_SALARY.copy()
    additional_salary_data['user_id'] = user_register_response.json()['user_id']

    response = client.post(
        "/salary/",
        json=salary_data,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == status.HTTP_201_CREATED

    response = client.post(
        "/salary/",
        json=additional_salary_data,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == status.HTTP_201_CREATED

    # Пытаемся получить зарплату за текущего пользователя
    get_response = client.get(
        "/my_salary/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert get_response.status_code == status.HTTP_404_NOT_FOUND

    # Логинимся за созданного пользователя
    login_response = client.post(
        "/login/",
        data={"username": employee_user["email"], "password": employee_user["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert login_response.status_code == 200
    assert "access_token" in login_response.json()

    new_user_login_token = login_response.json()["access_token"]

    # Получаем зарплату авторизованного пользователя
    get_response = client.get(
        "/my_salary/",
        headers={"Authorization": f"Bearer {new_user_login_token}"}
    )

    data = get_response.json()
    assert get_response.status_code == status.HTTP_200_OK
    assert len(data) == 2
    assert all(salary["amount"] for salary in data)
    assert all(salary["user_id"] == salary_data["user_id"] for salary in data)
