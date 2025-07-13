import pytest


@pytest.fixture
def login_as_admin(client, admin_user):
    """Фикстура для получения авторизации в качестве администратора"""

    # Логинимся как админ (создан скриптом init_admin_user)
    login_response = client.post(
        "/login/",
        data={"username": admin_user["email"], "password": admin_user["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    return login_response.json()["access_token"]
