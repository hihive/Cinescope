import pytest

from models.base_models import RegisterUserResponse, UserDBModel
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
        assert response["user"]["email"] == test_user.email, "Email не совпадает"

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

    def test_register_user_db_session(self, api_manager, test_user, db_session):
        """
        Тест на регистрацию пользователя с проверкой в базе данных.
        """
        # выполняем запрос на регистрацию нового пользователя
        response = api_manager.auth_api.register_user(test_user)
        register_user_response = RegisterUserResponse(**response.json())

        # Проверяем добавил ли сервис Auth нового пользователя в базу данных
        users_from_db = db_session.query(UserDBModel).filter(UserDBModel.id == register_user_response.id)

        # получили обьект из бзы данных и проверили что он действительно существует в единственном экземпляре
        assert users_from_db.count() == 1, "обьект не попал в базу данных"
        # Достаем первый и единственный обьект из списка полученных
        user_from_db = users_from_db.first()
        # можем осуществить проверку всех полей в базе данных например Email
        assert user_from_db.email == test_user.email, "Email не совпадает"

        db_session.delete(user_from_db)
        db_session.commit()
