import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_get_users(client, login_as_admin, employee_user):
    """Тест для проверки эндпоинта для получения списка новых сотрудников"""

    # Логинимся как админ
    token = login_as_admin

    # Регистрируем нового сотрудника
    register_response = client.post(
        "/register/",
        json=employee_user,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert register_response.status_code == status.HTTP_201_CREATED

    # Получаем список сотрудников
    get_response = client.get(
        "/users/",
        headers={"Authorization": f"Bearer {token}"}
    )

    data = get_response.json()
    assert get_response.status_code == status.HTTP_200_OK
    assert len(data) == 2
    assert all(user["email"] for user in data)
    assert any(user["email"] == employee_user["email"] for user in data)
