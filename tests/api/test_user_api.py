import pytest

from models.base_models import RegisterUserResponse


class TestUser:
    def test_create_user(self, api_manager, super_admin, creation_user_data):
        """
        Тест на создание пользователя
        """
        # Создаю пользователя через супер админа
        response = super_admin.api.user_api.create_user(creation_user_data)

        # Десериализую ответ в объект RegisterUserResponse
        created_user = RegisterUserResponse(**response.json())

        # Проверка данных
        assert created_user.verified is True

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        """
        Тест на получение юзера по заданным параметрам
        """
        # Создаю пользователя через супер админа
        response = super_admin.api.user_api.create_user(creation_user_data)

        # Десериализую ответ в объект RegisterUserResponse
        user = RegisterUserResponse(**response.json())

        # Получаю пользователя по id созданного ранее пользователя
        response_by_id = super_admin.api.user_api.get_user(user.id)

        # Десериализую ответ в объект RegisterUserResponse
        user_by_id = RegisterUserResponse(**response_by_id.json())

        # Получаю пользователя по email созданного ранее пользователя
        response_by_email = super_admin.api.user_api.get_user(user.email)

        # Десериализую ответ в объект RegisterUserResponse
        user_by_email = RegisterUserResponse(**response_by_email.json())

        # Проверка данных
        assert user == user_by_id == user_by_email, "Содержание ответов должно быть идентичным"

    @pytest.mark.slow
    def test_get_user_by_id_common_user(self, common_user):
        """
        Негативный тест
        Получение пользователя по email без имеющихся на это прав
        """
        common_user.api.user_api.get_user(common_user.email, expected_status=403)
