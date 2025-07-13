import pytest

INCORRECT_USER_DATA = {'username': 'fake_admin', 'password': 'fake_secret_password'}


@pytest.mark.asyncio
async def test_login_with_correct_credentials(client, admin_user):
    """Тест для проверки авторизации с корректными данными"""

    # Логинимся как админ (создан скриптом init_admin_user)
    login_response = client.post(
        "/login/",
        data={"username": admin_user["email"], "password": admin_user["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


@pytest.mark.asyncio
async def test_login_with_incorrect_credentials(client):
    """Тест для проверки авторизации с некорректными данными"""

    # Логинимся как админ (создан скриптом init_admin_user)
    login_response = client.post(
        "/login/",
        data=INCORRECT_USER_DATA,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert login_response.status_code == 401
