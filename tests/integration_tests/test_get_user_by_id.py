import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_get_user_by_id(client, login_as_admin, employee_user):
    """Тест для проверки эндпоинта для получения сотрудника по ID"""

    # Логинимся как админ
    token = login_as_admin

    # Регистрируем нового сотрудника
    register_response = client.post(
        "/register/",
        json=employee_user,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert register_response.status_code == status.HTTP_201_CREATED
    registered_user_id = register_response.json()['user_id']

    # Получаем сотрудника по ID
    response = client.get(
        f"/users/{registered_user_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data['email'] == employee_user['email']
    assert data['first_name'] == employee_user['first_name']
    assert data['last_name'] == employee_user['last_name']
    assert data['role'] == employee_user['role']
