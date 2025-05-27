import pytest

from models.base_models import RegisterUserResponse
from resources.user_creds import SuperAdminCreds


class TestAuthAPI:
    def test_register_user(self, api_manager, test_user):
        """
        Тест на регистрацию пользователя.
        """
        # Регистрирую нового пользователя
        response = api_manager.auth_api.register_user(test_user)

        # Десериализую ответ в объект RegisterUserResponse
        register_user_response = RegisterUserResponse(**response.json())

        # Проверки
        assert register_user_response.email == test_user.email, "Email не совпадает"

    @pytest.mark.slow
    def test_register_and_login_user(self, api_manager, test_user):
        """
        Тест на регистрацию и авторизацию пользователя.
        """
        # Регистрация пользователя
        api_manager.auth_api.register_user(test_user)

        # Получаю email и password для последующего входа
        login_data = {"email": test_user.email, "password": test_user.password}

        # Отправляю запрос на авторизацию пользователя
        response = api_manager.auth_api.login_user(login_data).json()

        # Проверки
        assert "accessToken" in response, "Токен доступа отсутствует в ответе"
        assert  response["user"]["email"] == test_user.email, "Email не совпадает"


    @pytest.mark.parametrize("email, password, expected_status", [
        (f"{SuperAdminCreds.USERNAME}", f"{SuperAdminCreds.PASSWORD}", 200),
        ("test_login1@email.com", "asdqwe123Q!", 401),
        ("", "password", 401),
    ], ids=["Admin login", "Invalid user", "Empty username"])
    def test_login(self, email, password, expected_status, api_manager):
        """
        Тест авторизацию пользователя по различным валидным и невалидным параметрам входа.
        """
        login_data = {
            "email": email,
            "password": password
        }
        # Отправляю запрос на авторизацию пользователя
        api_manager.auth_api.login_user(login_data=login_data, expected_status=expected_status)
