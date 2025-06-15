import datetime
from datetime import timezone

import allure
import pytest

from conftest import test_movie_data, common_admin, super_admin
from constants.constants import INVALID_MOVIE_ID
from models.base_models import MovieDBModel, MoviesDataResponse


@allure.epic("Тестирование работы MoviesAPI")
class TestMoviesAPI:
    @allure.title("Тест на получение информации о фильмах.")
    @allure.description("""
        Этот тест проверяет наличие информации о фильмах в сервисе.
        Шаги:
        1. Получение полного списка фильмов без фильтра для поиска.
        2. Проверка данных.
        """)
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_movies(self, api_manager):
        """
        Тест на получение информации о фильмах
        """
        with allure.step("Получение полного списка фильмов без фильтра для поиска"):
            response = api_manager.movies_api.get_movies()

        with allure.step("Проверка, что фильмы есть в базе"):
            assert isinstance(response.json()["movies"], list)

    @allure.title("Тест на получение информации о фильмах c фильтром для поиска.")
    @allure.description("""
        Этот тест проверяет наличие информации о фильмах в сервисе с фильтром для поиска.
        Шаги:
        1. Получение списка фильмов c фильтром для поиска.
        2. Проверка данных на соответствие фильтру.
        """)
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("params", [
        {"minPrice": 10, "maxPrice": 50, "genreId": 1},
        {"minPrice": 100, "maxPrice": 200, "genreId": 3}
    ])
    def test_get_movies_with_params(self, api_manager, params):
        """
        Тест на получение информации о фильмах с фильтром
        """
        with allure.step("Получение списка фильмов c фильтром для поиска"):
            response = api_manager.movies_api.get_movies(params).json()

        with allure.step("Проверка данных на соответствие фильтру"):
            for movie in response["movies"]:
                assert (params["minPrice"] < movie["price"] < params["maxPrice"]), "Ошибка фильтрации по полю price"
                assert movie["genreId"] == params["genreId"], "Ошибка фильтрации по полю genreId"

    @allure.title("Тест на создание фильма")
    @allure.description("""
    Этот тест проверяет создание фильма и фильма только с обязательными полями.
    Шаги:
    1. Активация фикстур переданные через parametrize.
    2. Создание фильма с валидными данными".
    3. Десериализация ответа в объект MoviesDataResponse.
    4. Проверка данных.
    5. Удаление фильма после тестов.
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("data", [
        "test_movie_data",
        "test_movie_min_data_item",
    ], ids=["data", "min_data"])
    def test_create_movie(self, data, super_admin, request):
        """
        Тест на создание фильма
        """
        with allure.step("Активация фикстур переданные через parametrize"):
            data_fixture = request.getfixturevalue(data)

        with allure.step("Создание фильма с валидными данными"):
            response = super_admin.api.movies_api.create_movie(data_fixture)

        with allure.step("Десериализация ответа в объект MoviesDataResponse"):
            movie = MoviesDataResponse(**response.json())

        with allure.step("Проверка данных"):
            assert movie.name == data_fixture.name, "Название фильмов не совпадает"

        with allure.step("Удаление фильма после тестов"):
            super_admin.api.movies_api.delete_movie(movie.id)

    @allure.title("Тест на обновление фильма")
    @allure.description("""
    Этот тест проверяет обновление фильма.
    Шаги:
    1. Создание фильма через фикстуру.
    2. Обновление фильма.
    3. Десериализация ответа в объект MoviesDataResponse.
    4. Проверка, что фильм обновился.
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_movie(self, test_movie_for_update_data, create_movie_for_tests, super_admin):
        """
        Тест на обновление фильма
        """
        with allure.step("Создание фильма через фикстуру"):
            movie = create_movie_for_tests

        with allure.step("Обновление фильма"):
            updated_movie = super_admin.api.movies_api.update_movie(movie["id"], test_movie_for_update_data).json()

        with allure.step("Десериализация ответа в объект MoviesDataResponse"):
            updated_movie = MoviesDataResponse(**updated_movie)

        with allure.step("Проверка, что фильм обновился"):
            assert movie["name"] != updated_movie.name, "Фильмы совпадают"

    @allure.title("Тест на удаление фильма")
    @allure.description("""
    Этот тест проверяет удаление фильма.
    Шаги:
    1. Создание фильма через фикстуру и получение его ID.
    2. Успешное удаление фильма с валидным ID.
    3. Проверка, что фильм больше не доступен.
    """)
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_movie(self, create_movie_for_delete_test, super_admin):
        """
        Тест на удаление фильма
        """
        with allure.step("Создание фильма через фикстуру и получение его ID"):
            movie = create_movie_for_delete_test
            movie_id = movie.id

        with allure.step("Успешное удаление фильма с валидным ID"):
            super_admin.api.movies_api.delete_movie(movie_id)

        with allure.step("Проверка, что фильм больше не доступен"):
            super_admin.api.movies_api.get_movie(movie_id, expected_status=404)

    @allure.title("Тест на удаление фильмов всеми видами пользователей")
    @allure.description("""
    Этот тест проверяет удаление фильма всеми видами пользователей.
    Шаги:
    1. Активация фикстур переданные через parametrize.
    2. Создание тестового фильм.
    3. Успешное удаление фильма с валидным ID.
    4. Чистка после пользователей у которых нет прав на удаление фильмов.
    5. Проверка, что фильм действительно был удален.
    """)
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.slow
    @pytest.mark.parametrize("user,expected_status", [
        ("common_user", 403),
        ("common_admin", 403),
        ("super_admin", 200)
    ], ids=["User", "Admin", "SuperAdmin"])
    def test_delete_movie_all_users(self, super_admin, create_movie_for_delete_test, user, expected_status, request):
        """
        Тест на удаление фильмов всеми видами пользователей
        """
        with allure.step("Активация фикстур переданные через parametrize"):
            user_fixture = request.getfixturevalue(user)

        with allure.step("Создание тестового фильм"):
            movie = create_movie_for_delete_test
            movie_id = movie.id

        with allure.step("Удаление фильма с валидным ID"):
            user_fixture.api.movies_api.delete_movie(movie_id, expected_status=expected_status)

        with allure.step("Чистка после пользователей у которых нет прав на удаление фильмов"):
            if expected_status == 403:
                super_admin.api.movies_api.delete_movie(movie_id)

        with allure.step("Проверка, что фильм действительно был удален"):
            user_fixture.api.movies_api.get_movie(movie_id, expected_status=404)

    @allure.title("Тест на проверку работы БД при создании и удалении фильма")
    @allure.description("""
    Этот тест проверяет работу БД при создании и удалении фильма.
    Шаги:
    1. Подготовка тестовых данных.
    2. Проверка, что на данный момент такого фильма нет в БД.
    3. Создание тестового фильма.
    4. Проверка, что запись о фильме появилась в бд.
    5. Проверка, что сервис заполнил верно created_at с погрешностью в 5 минут.
    6. Удаление тестового фильм из базы данных.
    7. Проверка, что в конце тестирования фильма с таким названием действительно нет в базе.
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_delete_movie(self, super_admin, db_session, test_movie_data):
        """
        Тест на проверку работы БД при создании и удалении фильма
        """

        with allure.step("Подготовка тестовых данных"):
            movie = test_movie_data

        with allure.step("Проверка, что на данный момент такого фильма нет в БД"):
            movies_from_db = db_session.query(MovieDBModel).filter(MovieDBModel.name == movie.name)
            assert movies_from_db.count() == 0, "В базе уже присутствует фильм с таким названием"

        with allure.step("Создание тестового фильма"):
            response = super_admin.api.movies_api.create_movie(movies_data=movie)
            assert response.status_code == 201, "Фильм должен успешно создаться"
            created_movie = MoviesDataResponse(**response.json())

        with allure.step("Проверка, что запись о фильме появилась в бд"):
            movies_from_db = db_session.query(MovieDBModel).filter(MovieDBModel.name == created_movie.name)
            assert movies_from_db.one(), "В базе уже присутствует фильм с таким названием"
            movie_from_db = movies_from_db.first()

        with allure.step("Проверка что сервис заполнил верно created_at с погрешностью в 5 минут"):
            assert movie_from_db.created_at >= (
                    datetime.datetime.now(timezone.utc).replace(tzinfo=None) - datetime.timedelta(minutes=5)
            ), "Сервис выставил время создания с большой погрешностью"

        with allure.step("Удаление тестового фильм из базы данных"):
            super_admin.api.movies_api.delete_movie(movie_id=created_movie.id)

        with allure.step("Проверка, что в конце тестирования фильма с таким названием действительно нет в базе"):
            movies_from_db = db_session.query(MovieDBModel).filter(MovieDBModel.name == created_movie.name)
            assert movies_from_db.count() == 0, "Фильм не был удален из базы!"

    # INVALID TESTS
    @allure.title("Тест на получение информации о фильме по несуществующему id")
    @allure.description("""
    Этот тест проверяет получение информации о фильме по несуществующему id.
    Шаги:
    1. Получение фильма с невалидным ID.
    """)
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.slow
    def test_get_invalid_movie(self, api_manager, create_movie_for_tests):
        """
        Тест на получение информации о фильме по несуществующему id
        """
        with allure.step("Получение фильма с невалидным ID"):
            api_manager.movies_api.get_movie(INVALID_MOVIE_ID, expected_status=404)

    @allure.title("Тест на создание фильма без обязательных полей")
    @allure.description("""
    Этот тест проверяет создание фильма без обязательных полей.
    Шаги:
    1. Создание фильма с отсутствием обязательных полей.
    """)
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_invalid_movie(self, super_admin, test_movie_negative_data):
        """
        Тест на создание фильма без обязательных полей
        """
        with allure.step("Создание фильма с отсутствием обязательных полей"):
            super_admin.api.movies_api.create_movie(test_movie_negative_data, expected_status=400)

    @allure.title("Тест на создание фильма незарегистрированным пользователем")
    @allure.description("""
    Этот тест проверяет создание фильма незарегистрированным пользователем.
    Шаги:
    1. Создание фильма незарегистрированным пользователем.
    """)
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_movie_with_unauthorization_user(self, api_manager, test_movie_data):
        """
        Тест на создание фильма незарегистрированным пользователем
        """
        with allure.step("Создание фильма незарегистрированным пользователем"):
            api_manager.movies_api.create_movie(test_movie_data, expected_status=401)

    @allure.title("Тест на создание фильма пользователем без прав доступа")
    @allure.description("""
    Этот тест проверяет создание фильма пользователем без прав доступа.
    Шаги:
    1. Создание фильма с пользователем без прав доступа.
    """)
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.slow
    def test_create_movie_without_access_user(self, common_admin, test_movie_data):
        """
        Тест на создание фильма пользователем без прав доступа
        """
        with allure.step("Создание фильма с пользователем без прав доступа"):
            common_admin.api.movies_api.create_movie(test_movie_data, expected_status=403)

    @allure.title("Тест на обновление несуществующего фильма")
    @allure.description("""
    Этот тест проверяет обновление несуществующего фильма.
    Шаги:
    1. Изменение фильма с невалидным ID.
    """)
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_invalid_movie(self, super_admin, test_movie_data):
        """
        Тест на обновление несуществующего фильма
        """
        with allure.step("Изменение фильма с невалидным ID"):
            super_admin.api.movies_api.update_movie(INVALID_MOVIE_ID, test_movie_data, expected_status=404)

    @allure.title("Тест на удаление несуществующего фильма")
    @allure.description("""
    Этот тест проверяет удаление несуществующего фильма.
    Шаги:
    1. Удаление фильма с невалидным ID.
    """)
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_invalid_movie(self, super_admin):
        """
        Тест на удаление несуществующего фильма
        """
        with allure.step("Удаление фильма с невалидным ID"):
            super_admin.api.movies_api.delete_movie(INVALID_MOVIE_ID, expected_status=404)
