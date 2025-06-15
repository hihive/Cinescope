import allure
import pytest

from models.base_models import RegisterUserResponse


@allure.epic("Тестирование работы UsersAPI")
@allure.feature("Тестирование создания и получения юзера по конкретным параметрам")
class TestUser:
    @allure.title("Тест на создание пользователя с правами SuperUser")
    @allure.description("""
    Этот тест проверяет корректность создания пользователя с правами SuperUser.
    Шаги:
    1. Создание пользователя с правами SuperUser.
    2. Получение созданного пользователя по заданным параметрам.
    3. Проверка данных.
    4. Удаление пользователя после теста.
    """)
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user(self, api_manager, super_admin, creation_user_data):
        """
        Тест на создание пользователя
        """
        with allure.step("Создание пользователя через супер админа"):
            response = super_admin.api.user_api.create_user(creation_user_data)

        with allure.step("Десериализация ответа в объект RegisterUserResponse"):
            user = RegisterUserResponse(**response.json())

        with allure.step("Проверка данных"):
            assert user.verified is True

        with allure.step("Удаление пользователя после теста"):
            super_admin.api.user_api.delete_user(user.id)

    @allure.title("Тест на получение юзера по заданным параметрам")
    @allure.description("""
    Этот тест проверяет получение пользователя по заданным параметрам.
    Шаги:
    1. Создание пользователя с правами SuperUser.
    2. Десериализация ответа в объект RegisterUserResponse.
    3. Получаю пользователя по id созданного ранее пользователя.
    4. Десериализация ответа в объект RegisterUserResponse.
    5. Получаю пользователя по email созданного ранее пользователя.
    6. Десериализация ответа в объект RegisterUserResponse.
    7. Проверка данных
    """)
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_user_by_locator(self, super_admin, creation_user_data):
        """
        Тест на получение юзера по заданным параметрам
        """
        with allure.step("Создание пользователя через супер админа"):
            response = super_admin.api.user_api.create_user(creation_user_data)

        with allure.step("Десериализация ответа в объект RegisterUserResponse"):
            user = RegisterUserResponse(**response.json())

        with allure.step("Получаю пользователя по id созданного ранее пользователя"):
            response_by_id = super_admin.api.user_api.get_user(user.id)

        with allure.step("Десериализация ответа в объект RegisterUserResponse"):
            user_by_id = RegisterUserResponse(**response_by_id.json())

        with allure.step("Получаю пользователя по email созданного ранее пользователя"):
            response_by_email = super_admin.api.user_api.get_user(user.email)

        with allure.step("Десериализация ответа в объект RegisterUserResponse"):
            user_by_email = RegisterUserResponse(**response_by_email.json())

        with allure.step("Проверка данных"):
            assert user == user_by_id == user_by_email, "Содержание ответов должно быть идентичным"

        with allure.step("Удаление пользователя после теста"):
            super_admin.api.user_api.delete_user(user.id)

    @allure.title("Тест на получение пользователя по email без имеющихся на это прав")
    @allure.description("""
    Негативный тест
    Этот тест проверяет получение пользователя по email без имеющихся на это прав.
    Шаги:
    1. Активация фикстур переданные через parametrize.
    2. Создание пользователя бе прав SuperUser.
    """)
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.slow
    @pytest.mark.parametrize("user", [
        "common_user", "common_admin"
    ], ids=["USER", "ADMIN"])
    def test_get_user_by_id_common_user(self, user, request):
        """
        Негативный тест
        Получение пользователя по email без имеющихся на это прав
        """
        with allure.step("Активация фикстур переданные через parametrize"):
            user_fixture = request.getfixturevalue(user)

        with allure.step("Создание пользователя бе прав SuperUser"):
            user_fixture.api.user_api.get_user(user_fixture.email, expected_status=403)
